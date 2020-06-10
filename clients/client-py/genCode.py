import sys
import os
import json
import six
import pprint
import py_compile
try:
    import pypandoc
except:
    pypandoc = None

# The python2 interpreter's repr function will use u'string' formats for its
# pprint module, which works with the python3 interpreter, but causes a problem
# when the py_compile.compile method is called in this file as a test.
#if six.PY2:
#    sys.stderr.write('Code generation requires python3 interpreter\n')
#    exit(1)

apiConfig = None
with open('apis.json') as f:
    apiConfig = json.load(f)


def cleanDocstring(old, indent=0):
    new = old
    new = old.replace('"""', '\"\"\"')
    new = new.replace('\'\'\'', '\\\'\\\'\\\'')
    # What we really ought to do here is create a list of fixup regexes for
    # common problems in the markup.  Examples of bad text include:
    #   -  '  * list'
    #   -  ``` then a newline
    new = new.replace('```js', '```')
    new = new.replace('```javascript', '```')
    new = new.split('\n')
    new.insert(0, '"""')
    new.append('"""')
    new.append('')
    # Basically this comprehension is so we don't get empty lines...
    new = [' ' * indent + x if x.strip() != '' else '' for x in new]
    return '\n'.join(new)


def createStaticClient(name, api, genAsync=False):
    api = api['reference']

    docstring = api.get('description')

    # Generate the first part of the class, basically just import the BaseClient
    # class
    baseModule = '.asyncclient' if genAsync else '.client'
    baseClass = 'AsyncBaseClient' if genAsync else 'BaseClient'
    lines = [
        '# coding=utf-8',
        '#####################################################',
        '# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #',
        '#####################################################',
        '# noqa: E128,E201'
        '',
        'from %s import %s' % (baseModule, baseClass),
        'from %s import createApiClient' % baseModule,
        'from %s import config' % baseModule,
        'from %s import createTemporaryCredentials' % baseModule,
        'from %s import createSession' % baseModule,
        '_defaultConfig = config',
        '',
        '',
    ]

    lines.append('class %s(%s):' % (name, baseClass))

    # If the API has a description, we'll make that be the docstring.  We want
    # to process the docstring so that it's a """ string in Python with the
    # correct indentation.  Also escape triple quotes so that it's not easy
    # to break out of the docstring accidentally
    if docstring:
        lines.append(cleanDocstring(docstring, indent=4))

    lines.append('    classOptions = {')

    # apply a default for apiVersion; this can be removed when all services have
    # been upgraded to provide apiVersion
    if 'apiVersion' not in api:
        api['apiVersion'] = 'v1'

    copiedOptions = ('exchangePrefix',)
    for opt in copiedOptions:
        if api.get(opt):
            lines.append('        "%s": "%s",' % (opt, api[opt]))
    lines.append('    }')

    copiedProperties = ('serviceName', 'apiVersion')
    for opt in copiedProperties:
        if api.get(opt):
            lines.append('    %s = %s' % (opt, repr(api[opt])))
    lines.append('')

    # We need to build up some information about how the functions work
    functionInfo = {}

    for entry in api['entries']:
        if entry['type'] == 'function':
            # We don't want to burn in the full api reference for each thing as
            # the dictionary parameter, since we'll be using some of these for
            # the code formatting (e.g. docstring)
            #
            # Sometimes, mandatory fields are hardcoded at declaration and
            # optional are copied in with a loop
            funcRef = {
                'args': entry['args'],
                'name': entry['name'],
                'route': entry['route'],
                'method': entry['method'],
            }
            for key in ['stability', 'query', 'input', 'output']:
                if (entry.get(key)):
                    funcRef[key] = entry[key]

            functionInfo[entry['name']] = funcRef
            # Let's genereate a docstring, but only if it's got some meat
            docstring = 'This method has no documentation, womp womp'
            if entry.get('description'):
                ds = entry.get('description', '')
                if entry.get('title'):
                    ds = entry.get('title') + '\n\n' + ds
                if entry.get('stability'):
                    ds = '%s\n\nThis method is ``%s``' % (ds, entry['stability'])

                docstring = cleanDocstring(ds, indent=8)

            if genAsync:
                lines.extend([
                    '    async def %s(self, *args, **kwargs):' % entry['name'],
                    docstring,
                    '        return await self._makeApiCall(self.funcinfo["%s"], *args, **kwargs)' % entry['name'],
                    ''
                ])
            else:
                lines.extend([
                    '    def %s(self, *args, **kwargs):' % entry['name'],
                    docstring,
                    '        return self._makeApiCall(self.funcinfo["%s"], *args, **kwargs)' % entry['name'],
                    ''
                ])
        elif entry['type'] == 'topic-exchange':
            # We don't want to burn in the full api reference for each thing as
            # the dictionary parameter, since we'll be using some of these for
            # the code formatting (e.g. docstring)
            #
            # Sometimes, mandatory fields are hardcoded at declaration and
            # optional are copied in with a loop
            exRef = {
                'exchange': entry['exchange'],
                'name': entry['name'],
                'routingKey': entry['routingKey'],
            }
            for key in ['schema']:
                if (entry.get(key)):
                    exRef[key] = entry[key]

            # Let's genereate a docstring, but only if it's got some meat
            if entry.get('description'):
                ds = entry.get('description', '')
                if entry.get('title'):
                    ds = entry.get('title') + '\n\n' + ds
                if entry.get('stability'):
                    ds = '%s\n\nThis method is ``%s``' % (ds, entry['stability'])

                ds += '\n\nThis exchange takes the following keys:'
                for key in entry['routingKey']:
                    ds += '\n\n * %s: %s%s' % (key.get('name'), key.get('summary', ''), ' (required)' if key['required'] else '')

            lines.append('    def %s(self, *args, **kwargs):' % entry['name'])
            lines.append(cleanDocstring(ds, indent=8))
            lines.append('        ref = {')
            for refK, refV in sorted(six.iteritems(exRef)):
                if refK == 'routingKey':
                    lines.append('            \'routingKey\': [')
                    for routingKey in refV:
                        lines.append('                {')
                        for routingK, routingV in sorted(six.iteritems(routingKey)):
                            if routingK in ('name', 'constant', 'multipleWords'): 
                                lines.append('                    \'%s\': %s,' % (routingK, pprint.pformat(routingV)))
                        lines.append('                },')
                    lines.append('            ],')
                else:
                    lines.append('            \'%s\': %s,' % (refK, pprint.pformat(refV)))
            lines.append('        }')
            lines.append('        return self._makeTopicExchange(ref, *args, **kwargs)')
            lines.append('')

    lines.append('    funcinfo = {')

    for funcname, ref in sorted(six.iteritems(functionInfo)):
        lines.append('        "%s": {' % funcname)
        for keyname, keyvalue in sorted(six.iteritems(ref)):
            lines.append('            \'%s\': %s,' % (keyname, pprint.pformat(keyvalue)))
        lines.append('        },')
    lines.append('    }')

    lines.extend([
        '',
        '',
        '__all__ = %s' % repr([
            'createTemporaryCredentials',
            'config',
            '_defaultConfig',
            'createApiClient',
            'createSession',
            name
        ]),
        '',
    ])

    # Join the lines, then re-split them because some embedded new lines need
    # to be addressed
    lines = '\n'.join(lines)
    lines = lines.split('\n')

    # Clean up trailing whitespace
    lines = [x.rstrip() for x in lines]

    # Build the final string
    return '\n'.join(lines)


# List of files which we've created for the build and release system's
# consumption
filesCreated = []

# The lines of the _client_importer.py file for sync clients
syncImporterLines = []

# The lines of the _client_importer.py file for async clients
asyncImporterLines = []

for name, api in apiConfig.items():
    syncfilename = os.path.join('taskcluster', name.lower() + '.py')
    asyncfilename = os.path.join('taskcluster', 'aio', name.lower() + '.py')

    syncClientString = createStaticClient(name, api)
    asyncClientString = createStaticClient(name, api, genAsync=True)

    syncImporterLines.append('from .%s import %s  # NOQA' % (name.lower(), name))
    asyncImporterLines.append('from .%s import %s  # NOQA' % (name.lower(), name))

    with open(syncfilename, 'wb') as f:
        if not six.PY2:
            py_compile.compile(syncfilename, doraise=True)
        f.write(syncClientString.encode('utf-8'))
        filesCreated.append(syncfilename)

    with open(asyncfilename, 'wb') as f:
        if not six.PY2:
            py_compile.compile(asyncfilename, doraise=True)
        f.write(asyncClientString.encode('utf-8'))
        filesCreated.append(asyncfilename)

syncImporterFilename = os.path.join('taskcluster', '_client_importer.py')
with open(syncImporterFilename, 'w') as f:
    syncImporterLines.sort()
    syncImporterLines.append('')
    filesCreated.append(syncImporterFilename)
    f.write('\n'.join(syncImporterLines))
    py_compile.compile(syncImporterFilename, doraise=True)

asyncImporterFilename = os.path.join('taskcluster', 'aio', '_client_importer.py')
with open(asyncImporterFilename, 'w') as f:
    asyncImporterLines.sort()
    asyncImporterLines.append('')
    filesCreated.append(asyncImporterFilename)
    f.write('\n'.join(asyncImporterLines))
    py_compile.compile(asyncImporterFilename, doraise=True)

with open('filescreated.dat', 'w') as f:
    f.write('\n'.join(filesCreated))

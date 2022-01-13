import json

from unomi_query_language.query.dispatcher import Host, Dispatcher
from unomi_query_language.query.parser import Parser
from unomi_query_language.query.grammar.grammars import read
from pprint import pprint

from unomi_query_language.query.transformers.select_transformer import SelectTransformer



p = Parser(read('uql_select.lark'), start='select')
t = p.parse(
    """
    SELECT PROFILE OFFSET 100 LIMIT 20
    """
)

query = SelectTransformer().transform(t)

#Connect to unomi

host = Host('18.179.200.236', port=8181, protocol='http').credentials('karaf','karaf')
dispatcher = Dispatcher(host)
response = dispatcher.fetch(query)

#Read response

if response.status_code == 200:
    pprint(json.loads(response.content))
else:
    print(response.content)
During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "get_polls.py", line 59, in <module>
    tkps =  pollScrapper()
  File "get_polls.py", line 15, in __init__
    self.get_polls_details()
  File "get_polls.py", line 21, in get_polls_details
    p = self.get_poll_results(poll)
  File "get_polls.py", line 40, in get_poll_results
    r = requests.get(poll_url) 
  File "/home/opc/.local/lib/python3.6/site-packages/requests/api.py", line 75, in get
    return request('get', url, params=params, **kwargs)
  File "/home/opc/.local/lib/python3.6/site-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/opc/.local/lib/python3.6/site-packages/requests/sessions.py", line 542, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/opc/.local/lib/python3.6/site-packages/requests/sessions.py", line 655, in send
    r = adapter.send(request, **kwargs)
  File "/home/opc/.local/lib/python3.6/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='tkpolls.com', port=443): Max retries exceeded with url: /results/2017-04-23-2140 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0xfffe7153dcf8>: Failed to establish a new connection: [Errno 110] Connection timed out',))


from starlette.requests import Request


def add_process_time_header(request: Request, call_next):

    response = await call_next(request)
    return response
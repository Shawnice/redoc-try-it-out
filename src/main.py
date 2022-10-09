from fastapi import FastAPI
from littletable import DataObject, Table
from starlette.responses import HTMLResponse

from src.models import Response, User

app = FastAPI(redoc_url=None)

USERS = Table("USERS")
USERS.create_index("id", unique=True)


@app.get("/user/{unique_id}")
async def get_user(user_id: str):
    for user_data in USERS.where(id=user_id):
        return Response(
            message=f"Username : {user_data.name}, email: {user_data.email_address}"
        )
    return Response(message="User not found!")


@app.post("/user")
async def add_user(user: User):
    if USERS.where(id=user.id):
        return Response(message=f"User: {user.name} already exists")
    USERS.insert(DataObject(**user.dict()))
    return Response(
        message=f"User: {user.name} has been created, unique ID is {user.id}"
    )


#
# @app.post("/message/send")
# async def send_message(message: TextMessage | PhotoMessage | AudioMessage):
#     return Response(message="Message sent!")


def get_redoc_html(
    *,
    openapi_url: str,
    title: str,
    redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: bool = True,
) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
        <link rel="shortcut icon" href="{redoc_favicon_url}">
        <!--
        ReDoc doesn't change outer page styles
        -->
        <style>
          body {{
            margin: 0;
            padding: 0;
          }}
        </style>
        </head>
        <body>
            <div id="redoc-container"></div>
              <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.55/bundles/redoc.standalone.min.js"> </script>
              <script src="https://cdn.jsdelivr.net/gh/wll8/redoc-try@1.4.1/dist/try.js"></script>
              <script>
                initTry({{
                openApi: `{openapi_url}`,
                  redocOptions: {{scrollYOffset: 50}},
                }})
              </script>
        </body>
        </html>
        """
    return HTMLResponse(html)


@app.get("/redoc", include_in_schema=False)
async def redoc_try_it_out() -> HTMLResponse:
    title = app.title + " Redoc with try it out"
    return get_redoc_html(openapi_url=app.openapi_url, title=title)

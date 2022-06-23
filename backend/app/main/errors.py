from . import main


# TODO:更新为json
@main.app_errorhandler(404)
def page_not_found(e):
    # 404
    pass


@main.app_errorhandler(500)
def internal_server_error(e):
    # 500
    pass
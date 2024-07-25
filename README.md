# Initialize
**Place the app folder to the desired path, then replace "app_path" string and run this in maya**

    app_path = "Path:/to/this/app"

    import sys, os
    os.environ['layout_tool_path'] = app_path
    if app_path not in sys.path: sys.path.append(app_path)

    import lay_run
    lay_run.run()
from flask import Flask, render_template, redirect, request
from website import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1") 
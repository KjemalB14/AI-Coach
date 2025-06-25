from flask import Flask, request, jsonify
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers
from ariadne.explorer import ExplorerGraphiQL
from ariadne import ObjectType

# Define types and resolvers
query = ObjectType("Query")


@query.field("hello")
def resolve_hello(*_):
    return "Hello, World!"


# Load schema from file
type_defs = load_schema_from_path("schema.graphql")

schema = make_executable_schema(
    type_defs,
    query,
    snake_case_fallback_resolvers
)

# Create Flask app
app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Serve GraphiQL playground on GET request
    explorer_html = ExplorerGraphiQL().html(None)
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # Process GraphQL queries
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)

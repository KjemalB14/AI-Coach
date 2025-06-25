# GraphQL Hello World API

A simple GraphQL API that returns "Hello, World!" when queried.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Access the GraphQL playground:
   - Open your browser and navigate to: http://127.0.0.1:5000/graphql
   - Try this query:
   ```graphql
   {
     hello
   }
   ```

## Project Structure

- `app.py`: Main application file with Flask and GraphQL setup
- `requirements.txt`: Python dependencies
- `schema.graphql`: GraphQL schema definition
- `test.py`: Unit tests for the API

## Testing

Run the tests with:

```bash
python -m unittest test.py
```

## Notes

- This project uses Ariadne 0.20.1 which includes the `ExplorerGraphiQL` class instead of the older `PLAYGROUND_HTML` constant.
- If you encounter import errors, make sure your Ariadne version matches the one specified in requirements.txt.

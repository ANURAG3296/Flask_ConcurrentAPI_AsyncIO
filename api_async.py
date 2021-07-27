from flask import Flask, request, json, jsonify
import requests
import asyncio
import aiohttp


app = Flask(__name__)

sortBy_criteria = ['id', 'reads', 'likes', 'popularity']
sortBy_direction = ['asc', 'desc']
tag_Options = ['tech', 'science', 'history', 'health']
url = 'https://api.hatchways.io/assessment/blog/posts?tag='
cache = {}
unique_values = {}


@app.route("/api/ping", methods=['GET'])
def route_one():
    return jsonify({"success": True}), 200


@app.route("/api/posts", methods=['GET'])
def route_two():
    if 'tags' not in request.args or request.args['tags'].strip() == '':
        return error_response("Tags parameter is required", 400)

    sort_by = get_sort_by()
    if sort_by == 0:
        return error_response("sortBy parameter is invalid", 400)

    direction = get_direction()
    if direction == 0:
        return error_response("direction Parameter is invalid", 400)

    list_tags = set(request.args['tags'].split(','))
    responses = asyncio.run(get_data_from_api(list_tags))
    sorted_data = sorting_values(responses, sort_by, direction)
    return jsonify({"posts": sorted_data})


# Calling api's concurrently
def concurrent_call_to_api(session, list_tags):
    raw_data = []
    for tag in list_tags:
        if tag not in cache:
            raw_data.append(asyncio.create_task(session.get(url + tag, ssl=False)))
            cache[tag] = raw_data
    return raw_data


async def get_data_from_api(list_tags):
    async with aiohttp.ClientSession() as session:
        tasks = concurrent_call_to_api(session, list_tags)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            single_response = await response.json()
            for item in single_response['posts']:
                unique_values[item['id']] = item
        return unique_values


# Method to sort values and set sort direction based on the URL
def sorting_values(response, sort_by, direction):
    formatted = json.dumps(response, indent=4)
    new_list = list(json.loads(formatted).values())
    return sorted(new_list, key=lambda x: x[sort_by], reverse=direction == "desc")


# get sortBy
def get_sort_by():
    if 'sortBy' not in request.args or request.args['sortBy'].strip() == '':
        return 'id'
    if request.args['sortBy'] not in sortBy_criteria:
        return 0
    return request.args['sortBy']


# get direction
def get_direction():
    if 'direction' not in request.args or request.args['direction'].strip() == '':
        return 'asc'
    if request.args['direction'] not in sortBy_direction:
        return 0
    return request.args['direction']


def error_response(message, code):
    return {"error": message}, code


if __name__ == '__main__':
    app.run(debug=True)
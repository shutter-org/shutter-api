from flask import request, jsonify

class CommentError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def comment(app) -> None:
    
    @app.route("/comment/<comment_id>/like", methods=["Post"])
    def postLikeComment(comment_id):
        
        data = request.get_json()
        try:
            like = data["like"]
            if type(like) is not bool:
                raise CommentError("like is not of boolean type")
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except CommentError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "like": like,
            "comment_id": comment_id
        }
        
        return jsonify(data), 200
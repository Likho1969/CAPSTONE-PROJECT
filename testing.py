# Likho Kapesi
# Classroom 2

import unittest
from app import app


# class for testing API route connection
class TestApiRoutes(unittest.TestCase):

    # testing registration connection
    def test_registration(self):  
        test_reg = app.test_client()
        response = test_reg.get('/registration/')
        status = response.status_code
        self.assertEqual(status, 405)

    # testing send email connection
    def test_send_email(self):  
        test_email = app.test_client()
        response = test_email.get('/send-email/<email>')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing login connection
    def test_login(self):  
        test_login = app.test_client()
        response = test_login.get('/login/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing view profile connection
    def test_viw_profile(self):  
        test_view = app.test_client()
        response = test_view.get('/view-profile/<username>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing edit profile connection
    def test_edit_profile(self):  
        test_edit = app.test_client()
        response = test_edit.get('/edit-profile/<username>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing delete profile connection
    def test_delete_profile(self):  
        test_delete = app.test_client()
        response = test_delete.get('/delete-profile/<username>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing display all users connection
    def test_display_all_users(self):
        test_display_all = app.test_client()
        response = test_display_all.get('/display-all-users/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing display one user connection
    def test_display_one_user(self):
        test_display_one = app.test_client()
        response = test_display_one.get('/display-one-user/<username>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing create post connection
    def test_create_post(self):
        test_post = app.test_client()
        response = test_post.get('/create-post/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing delete post connection
    def test_delete_post(self):
        test_del_post = app.test_client()
        response = test_del_post.get('/delete-post/<int:post_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing edit post connection
    def test_edit_post(self):
        test_edit_post = app.test_client()
        response = test_edit_post.get('/edit-post/<int:post_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing show posts connection
    def test_show_posts(self):
        show_posts = app.test_client()
        response = show_posts.get('/show-posts/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing show a specific post connection
    def test_show_a_post(self):
        show_a_post = app.test_client()
        response = show_a_post.get('/view-post/<int:post_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing show a specific user's posts connection
    def test_show_user_posts(self):
        show_users_posts = app.test_client()
        response = show_users_posts.get('/view-users-posts/<int:id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing like post connection
    def test_like_post(self):
        like_post = app.test_client()
        response = like_post.get('/like-post/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing display likes on a post connection
    def test_display_post(self):
        like_post = app.test_client()
        response = like_post.get('/display-likes/<int:post_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing add comment on a post connection
    def test_add_comment(self):
        add_comment = app.test_client()
        response = add_comment.get('/add-comment/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing display comments connection
    def test_display_comments(self):
        display_comments = app.test_client()
        response = display_comments.get('/display-comments/<post_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing edit a comment connection
    def test_edit_comment(self):
        edit_comment = app.test_client()
        response = edit_comment.get('/edit-comment/<int:comment_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing delete a comment connection
    def test_delete_comment(self):
        delete_comment = app.test_client()
        response = delete_comment.get('/delete-comment/<int:comment_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing add a reply connection
    def test_add_reply(self):
        add_reply = app.test_client()
        response = add_reply.get('/add-reply/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing display reply connection
    def test_display_reply(self):
        display_reply = app.test_client()
        response = display_reply.get('/display-reply/<reply_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing edit reply connection
    def test_edit_reply(self):
        edit_reply = app.test_client()
        response = edit_reply.get('/edit-reply/<int:reply_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    # testing edit reply connection
    def test_delete_reply(self):
        delete_reply = app.test_client()
        response = delete_reply.get('/delete-reply/<int:reply_id>/')
        status = response.status_code
        self.assertEqual(status, 404)


if __name__ == '__main__':
    test = TestApiRoutes()

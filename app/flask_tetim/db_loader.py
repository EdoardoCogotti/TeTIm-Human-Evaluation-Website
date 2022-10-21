import os
import json
import psycopg2
from flask_tetim.config import Config


class DatabaseLoader:

    tags = ["sampled_photo_landscape", "sampled_photo_animal", "sampled_photo_person",
            "sampled_photo_food", "sampled_painting_high-renaissance", "sampled_painting_baroque",
            "sampled_painting_neoclassicism", "sampled_art_digital", "sampled_art_traditional",
            "sampled_art_sketch"]
    models = ["real"]

    cur_dir = os.getcwd()
    num_elem = 30
    conf = Config()

    @staticmethod
    def create_connection():
        if DatabaseLoader.conf.DOCKER_FLAG:
            conn = psycopg2.connect(dbname="tetim", host="db", user="postgres", password="postgres")
        else:
            conn = psycopg2.connect(dbname="tetim", user="postgres", password="postgres")
        return conn

    @staticmethod
    def create_question(conn, q):
        """
        # Create a new question into the question table
        #:param conn:
        #:param q:
        #:return: question id
        """

        q_id = -1
        try:
            sql = ''' INSERT INTO question(caption,caption_ita,image_file,category)
                        VALUES(%s,%s,%s,%s) RETURNING id '''
            cur = conn.cursor()
            cur.execute(sql, q)
            q_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)

        return q_id

    def load(self):

        # create a database connection
        connection = self.create_connection()

        with connection:

            # check if question table is empty
            try:
                sql = "SELECT COUNT(*) FROM question"
                cur = connection.cursor()
                cur.execute(sql)
                empty_db = cur.fetchone()[0]
                connection.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as e:
                print(e)

            if empty_db != 0:
                return

            for model in self.models:
                for tag in self.tags:

                    if self.conf.DOCKER_FLAG:
                        file_path = self.cur_dir + "/flask_tetim/static/tetim/" + model + "/" + tag + "/annotations/"
                        print(self.cur_dir)
                        print(file_path)
                        print(os.listdir(file_path))
                    else:
                        file_path = self.cur_dir + "\\flask_tetim\\static\\tetim\\" + model + "\\" + tag + "\\annotations\\"

                    for i in range(self.num_elem):
                        filename = file_path + str(i) + ".json"
                        with open(filename) as fp:
                            data = json.load(fp)

                        question = {}
                        question["caption"] = data["caption"]
                        question["caption_ita"] = data["caption_ita"]
                        question["image_file"] = str(i)  # jpg if real, png otherwise
                        question["category"] = tag
                        question_tuple = (question["caption"], question["caption_ita"], question["image_file"], question["category"])
                        question_id = self.create_question(connection, question_tuple)
                        print(f"QUESTION {question_id}")

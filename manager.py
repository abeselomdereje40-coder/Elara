from database import get_connection
import sqlite3
from tools.knowledge_chunker import KnowledgeChunker

class memory_manager:
    def __init__(self):
        self.conn=get_connection()
        self.cursor=self.conn.cursor()

    def save_conversation(self,session_id,role,message):
        message=str(message)
        self.cursor.execute("""
        INSERT INTO conversation (session_id,role,message) VALUES(?,?,?)
        """,(session_id,role,message))
        self.conn.commit()

    def get_conversation(self,session_id,limit=100):
        self.cursor.execute("""
        SELECT role,message FROM conversation WHERE session_id = ? ORDER BY id ASC LIMIT ?
        """,(session_id,limit))
        rows=self.cursor.fetchall()
        return rows

    def get_projects(self):
        self.cursor.execute("""
        SELECT * FROM projects ORDER BY updated_at DESC
        """)
        return self.cursor.fetchall()

    def create_project(self,name,description="",priprity="medium"):
        self.cursor.execute("""
        INSERT INTO projects (name,description,status,priority)
        VALUES (?,?,?,?)
        """,(name,description,"Active",priprity))
        self.conn.commit()
        return self.cursor.lastrowid

    def find_fact(self,fact):
        self.cursor.execute("""
        SELECT * FROM facts WHERE fact = ?
        """,(fact,))
        return self.cursor.fetchone()

    def save_fact(self,fact,catagory,importance=1):
        existing=self.find_fact(fact)
        if existing:
            self.cursor.execute("""
            UPDATE facts SET importance=?,
            updated_at = CURRENT_TIMESTAMP WHERE id =?
            """,(importance,existing["id"]))
        else:
            self.cursor.execute("""
            INSERT INTO facts (fact,catagory,importance)
            VALUES(?,?,?) """,(fact,catagory,importance))
        self.conn.commit()

    def search_fact(self,message):
        words=message.lower().split()
        stop_word={
            "what","is","are","the","a","an","my","me","i","do","you","did","about",
            "tell","can","could","would","please","of","to","in","on","for"
        }
        keywords=[]
        for word in words:
            word=word.strip(".,?!")
            
            if word not in stop_word and len(word)>=3:
                keywords.append(word)
        found={}
        for keyword in keywords:
            self.cursor.execute("""
            SELECT * FROM facts WHERE fact LIKE ? ORDER BY importance DESC,updated_at DESC
            """,(f"%{keyword}%",))
            rows=self.cursor.fetchall()
            for row in rows:
                found[row["id"]]=row

        return list(
            found.values(),
        )
        

    def find_project(self,name):
        self.cursor.execute("""
        SELECT * FROM projects WHERE name=?
        """,(name,))
        return self.cursor.fetchone()

    def add_notes(self,project_id,note):
        self.cursor.execute("""    
        INSERT INTO project_notes (project_id,note)
        VALUES(?,?) """,(project_id,note))
        self.conn.commit()

    def find_notes(self,project_id):
        self.cursor.execute("""
        SELECT note FROM project_notes WHERE project_id = ? 
        ORDER BY timestamp ASC """,(project_id,))
        return self.cursor.fetchall()

    def project_state(self,name ="",vision= "",current_phase ="",current_module ="",current_goal = "",next_goal ="",completion =0):
        self.cursor.execute("""
        INSERT INTO project_state (
        name ,
        vision ,
        current_phase ,
        current_module ,
        current_goal ,
        next_goal ,
        completion) VALUES (?,?,?,?,?,?,?) """,(name,vision,current_phase,current_module,current_goal,next_goal,completion)
        )
        self.conn.commit()

    def get_project_state(self,name):
        self.cursor.execute("""
        SELECT * FROM project_state WHERE name = ?
        """,(name,))
        return self.cursor.fetchone()

    def update_project_state(self,name ="",current_phase ="Planning",current_module ="",current_goal = "",next_goal ="",completion =0):
        self.cursor.execute("""
        UPDATE project_state SET (
        current_phase ,
        current_module ,
        current_goal ,
        next_goal ,
        completion) VALUES (?,?,?,?,?) WHERE name=?""",(current_phase,current_module,current_goal,next_goal,completion,name)
        )
        self.conn.commit()

    def add_project_step(self,project_id,step_number,title,status="pending"):
        self.cursor.execute("""
        INSERT INTO project_plan(project_id,step_number,title,status)
        VALUES (?,?,?,?)""",(project_id ,step_number ,title ,status ))
        self.conn.commit()

    def get_plan(self,project_id):
        self.cursor.execute("""
        SELECT * FROM project_plan WHERE project_id = ? ORDER BY step_number""",(project_id,))
        return self.cursor.fetchall()

    def get_all_projects(self):
        self.cursor.execute("""
        SELECT * FROM projects ORDER BY updated_at DESC""")
        return self.cursor.fetchall()

    def get_all_facts(self):
        self.cursor.execute("""
        SELECT * FROM facts ORDER BY importance DESC,created_at DESC""")
        return self.cursor.fetchall()

    def delete_fact(self,fact_id):
        self.cursor.execute("""
         DELETE FROM facts WHERE id=?""",(fact_id,))
        self.conn.commit()

    def save_knowledge(self,title,content,source="",tags=""):
        self.cursor.execute("""
            INSERT INTO knowledge (title,content,source,tags) VALUES(?,?,?,?)
        """,(title,content,source,tags))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_knowledge(self):
        self.cursor.execute("""
        SELECT * FROM knowledge ORDER BY created_at DESC""")
        return self.cursor.fetchall()

    def delete_knowledge(self,knowledge_id):
        self.cursor.execute("""
         DELETE FROM knowledge WHERE id=?""",(knowledge_id,))
        self.conn.commit()

    def get_all_conversation(self):
        self.cursor.execute("""
        SELECT * FROM conversation ORDER BY timestamp ASC""")
        return self.cursor.fetchall()
#side bar chat history
    def get_chat_sessions(self):
        self.cursor.execute("""
        SELECT c.session_id,(SELECT u.message FROM conversation AS u WHERE u.session_id=c.session_id AND u.role = 'user' ORDER BY u.id ASC LIMIT 1)
        AS title,MIN(c.id) AS first_id FROM conversation AS c GROUP BY c.session_id ORDER BY first_id DESC
        """)
        return self.cursor.fetchall()

    def delete_conversation(self,session_id):
        self.cursor.execute("""
         DELETE FROM conversation WHERE session_id=?""",(session_id,))
        self.conn.commit()

    def search_knowledge(self,message):
        words=message.lower().split()
        stop_word={
            "what","is","are","the","a","an","my","me","i","do","you","did","about",
            "tell","can","could","would","please","of","to","in","on","for","from","this","that","does","document","file","say","does",
            "document","says"
        }
        keywords=[]
        for word in words:
            word=word.strip(".,?!")
            
            if word not in stop_word and len(word)>=3:
                keywords.append(word)
        found={}
        for keyword in keywords:
            self.cursor.execute("""
            SELECT * FROM knowledge WHERE title LIKE ? 
            OR content LIKE ? OR tags LIKE ?
            ORDER BY  created_at DESC
            """,(f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
            ))
            rows=self.cursor.fetchall()
            for row in rows:
                if isinstance(row,sqlite3.Row):
                    data=dict(row)
                else:
                    column=[
                        description[0] for description in self.cursor.description
                    ]
                    data=dict(zip(column,row))
                row_id=data["id"]
                if row_id not in found:
                    found[row_id]={
                        "data":data,
                        "score":0
                    }
                title=(data.get("title") or "").lower()
                content=(data.get("content") or "").lower()
                tags=(data.get("tags") or "").lower()

                if keyword in title:
                    found[row_id]["score"]+=5

                if keyword in tags:
                    found[row_id]["score"]+=3

                if keyword in content:
                    found[row_id]["score"]+=1

        result=sorted(
            found.values(),
            key = lambda item:item["score"],
            reverse=True
        )

        print("relevent score")
        for item in result:
            data=item["data"]
            print("row type:",type(data))
            score=item["score"]
            print(f"Id : {data['id']} | "
            f" Title : {data['title']} | "
            f" Score : {score}")

        return [item["data"] for item in result]

    def save_knowledge_chunks(self,knowledge_id,chunks,embeddings=None):

        for index, chunk in enumerate(chunks):

            embedding_blob = None

            if embeddings is not None:
                embedding_blob = embeddings[index].astype(
                    "float32"
                ).tobytes()

            self.cursor.execute("""
            INSERT INTO knowledge_chunks
            (
                knowledge_id,
                chunk_index,
                content,
                location,
                embedding
            )
            VALUES (?, ?, ?, ?, ?)
            """, (
                knowledge_id,
                index,
                chunk["content"],
                chunk["location"],
                embedding_blob
            ))

        self.conn.commit()

    def get_knowledge_chunks(self, knowledge_id):

        self.cursor.execute("""
        SELECT *
        FROM knowledge_chunks
        WHERE knowledge_id = ?
        ORDER BY chunk_index ASC
        """, (knowledge_id,))

        return self.cursor.fetchall()

    def delete_knowledge_chunks(self, knowledge_id):

        self.cursor.execute("""
        DELETE FROM knowledge_chunks
        WHERE knowledge_id = ?
        """, (knowledge_id,))

        self.conn.commit()

    def chunk_existing_knowledge(self):
        from tools.embedding_model import EmbeddingModel

        chunker = KnowledgeChunker()
        embedder=EmbeddingModel()

        self.cursor.execute("""
        SELECT id, title, content, source
        FROM knowledge
        ORDER BY id ASC
        """)

        documents = self.cursor.fetchall()

        total_documents = 0
        total_chunks = 0

        for document in documents:

            knowledge_id = document["id"]

            # Don't create duplicates
            self.cursor.execute("""
            SELECT COUNT(*) AS count
            FROM knowledge_chunks
            WHERE knowledge_id = ?
            """, (knowledge_id,))

            existing = self.cursor.fetchone()["count"]

            if existing > 0:
                print(
                    f"Skipping '{document['title']}' "
                    f"(already has {existing} chunks)"
                )
                continue

            source = document["source"] or ""
            extension = source.lower().split(".")[-1]

            if extension:
                file_type = extension
            else:
                file_type = None

            chunks = chunker.chunk_document(
                document["content"],
                file_type
            )

            texts=[
                chunk["content"]
                for chunk in chunks
            ]
            embeddings=embedder.embed_documents(texts)

            self.save_knowledge_chunks(
                knowledge_id,
                chunks,
                embeddings
            )

            total_documents += 1
            total_chunks += len(chunks)

            print(
                f"Chunked: {document['title']} "
                f"→ {len(chunks)} chunks"
            )

        print("")
        print("Chunking complete")
        print("Documents processed:", total_documents)
        print("Chunks created:", total_chunks)

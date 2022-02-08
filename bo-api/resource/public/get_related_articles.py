import datetime

from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_restful import Resource
from sqlalchemy import desc
from webargs import fields

from db.db import DB
from decorator.catch_exception import catch_exception
from utils.serializer import Serializer


class GetRelatedArticles(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @doc(tags=['public'],
         description='Get the news articles related to the provided article ID',
         responses={
             "200": {},
             "422": {"description": "The provided article ID does not exist or is not accessible"}
         })
    @use_kwargs({
        'include_tags': fields.Bool(required=False),
    }, location="query")
    @catch_exception
    def get(self, id_, **kwargs):

        act = self.db.tables["ArticleCompanyTag"]
        att = self.db.tables["ArticleTaxonomyTag"]

        # Fetch the info from the DB

        article = self.db.session.query(self.db.tables["Article"]) \
            .filter(self.db.tables["Article"].handle == id_) \
            .filter(self.db.tables["Article"].status == "PUBLIC") \
            .filter(self.db.tables["Article"].publication_date <= datetime.date.today()) \
            .all()

        if len(article) < 1:
            return "", "422 The provided article ID does not exist or is not accessible"

        # Fetch all the related articles

        company_tags = [t.company for t in self.db.get(act, {"article": article[0].id})]
        company_tag_articles = [] if len(company_tags) == 0 \
            else [t.article for t in self.db.get(act, {"company": company_tags})]
        taxonomy_tags = [t.taxonomy_value for t in self.db.get(att, {"article": article[0].id})]
        taxonomy_tag_articles = [] if len(taxonomy_tags) == 0 \
            else [t.article for t in self.db.get(att, {"taxonomy_value": taxonomy_tags})]

        article_ids = list(set(company_tag_articles + taxonomy_tag_articles))

        # Fetch the two earliest related articles

        query = self.db.session.query(self.db.tables["Article"]) \
            .filter(self.db.tables["Article"].id != article[0].id) \
            .filter(self.db.tables["Article"].id.in_(article_ids)) \
            .filter(self.db.tables["Article"].status == "PUBLIC") \
            .filter(self.db.tables["Article"].publication_date <= datetime.date.today()) \
            .filter(self.db.tables["Article"].type == "NEWS")

        related_articles = query \
            .order_by(desc(self.db.tables["Article"].publication_date)) \
            .limit(2) \
            .all()

        data = Serializer.serialize(related_articles, self.db.tables["Article"])

        if "include_tags" in kwargs and kwargs["include_tags"] is True:
            article_ids = [a["id"] for a in data]

            taxonomy_tags = self.db.get(self.db.tables["ArticleTaxonomyTag"], {"article": article_ids})
            company_tags = self.db.get(self.db.tables["ArticleCompanyTag"], {"article": article_ids})

            for a in data:
                a["taxonomy_tags"] = [t.taxonomy_value for t in taxonomy_tags if t.article == a["id"]]
                a["company_tags"] = [t.company for t in company_tags if t.article == a["id"]]

        return data, "200 "

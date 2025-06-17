import reflex as rx

config = rx.Config(
    app_name="project",
    module = "project.project",
    plugins=[rx.plugins.TailwindV3Plugin()],
    db_url = "postgresql://postgres.affvdaqzngusgmvamydc:qyvmo5-Foswaw-vervoz@aws-0-us-east-1.pooler.supabase.com:6543/postgres",
)
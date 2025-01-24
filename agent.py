from dataclasses import dataclass
from database import SessionLocal
from models import Asset
from contextlib import contextmanager
from sqlalchemy.sql import text
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

load_dotenv()


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class DatabaseConn:
    @classmethod
    async def asset_description(cls, *, id: int) -> str | None:
        with get_session() as session:
            user = session.query(Asset).filter_by(id=id).first()
            return user.name if user else None

    @classmethod
    async def asset_count(cls) -> int:
        with get_session() as session:
            sql = text("SELECT COUNT(*) FROM assets")
            record_count = session.execute(sql).scalar()
            return record_count

    # @classmethod
    # async def subscription_plan(cls, *, id: int) -> str:
    #     with get_session() as session:
    #         user = session.query(User).filter_by(id=id).first()
    #         return user.subscription_plan if user else "Free Plan"


@dataclass
class SupportDependencies:
    asset_id: int
    db: DatabaseConn


class SupportResult(BaseModel):
    asset_description: str = Field(description="Asset description returned to the user")
    # escalate_to_admin: bool = Field(description="Whether to escalate the query to an admin")
    # risk_level: int = Field(description="Risk level of the query", ge=0, le=10)


support_agent = Agent(
    "openai:gpt-4o",
    deps_type=SupportDependencies,
    result_type=SupportResult,
    system_prompt=(
        "You are a catalog search agent. Help users with their catalog searches, "
        "find data assets in the catlog."
    ),
)


@support_agent.tool
async def asset_count(ctx: RunContext[SupportDependencies]) -> str:
    """Returns the catalog's asset count."""

    count = await ctx.deps.db.asset_count()
    return f"The asset count is currently: {count}"


# @support_agent.system_prompt
# async def add_ser_name(ctx: RunContext[SupportDependencies]) -> str:
#     user_name = await ctx.deps.db.user_name(id=ctx.deps.user_id)
#     return f"The user's name is {user_name!r}"


# @support_agent.tool
# async def account_status(ctx: RunContext[SupportDependencies]) -> str:
#     """Returns the user's account status."""
#     status = await ctx.deps.db.account_status(id=ctx.deps.user_id)
#     return f"Your account is currently: {status}"


# @support_agent.tool
# async def subscription_plan(ctx: RunContext[SupportDependencies]) -> str:
#     """Returns the user's subscription plan."""
#     plan = await ctx.deps.db.subscription_plan(id=ctx.deps.user_id)
#     return f"Your current subscription plan is: {plan}"


async def test_support_agent():
    deps = SupportDependencies(asset_id=102, db=DatabaseConn())

    # Query 1: Subscription plan
    # result = await support_agent.run("What tree data exists in the catalog?", deps=deps)
    # Query 2: Asset count
    # result = await support_agent.run("How many assets are in the catalog?", deps=deps)
    # Query 3: Asset count
    result = await support_agent.run("Give me the asset count.", deps=deps)

    print(result.data)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_support_agent())

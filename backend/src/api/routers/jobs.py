from typing import Annotated, Optional
from uuid import UUID

from fastapi import HTTPException, Query
from fastapi.routing import APIRouter
from models import Job
from example_repo.jobs import JobsRepository

from api.db import DatabaseDep

router = APIRouter(
    prefix="/jobs",
)


@router.post("/")
async def create_job(
    job: Job,
    database: DatabaseDep = DatabaseDep,
) -> Job:
    jobs_repository = JobsRepository(database)
    return await jobs_repository.create(job)


@router.get("/")
async def get_jobs(
    job_ids: Annotated[Optional[list[UUID]], Query()] = None,
    database: DatabaseDep = DatabaseDep,
) -> list[Job]:
    jobs_repository = JobsRepository(database)
    if job_ids:
        return await jobs_repository.read_many(job_ids)
    else:
        return await jobs_repository.read_many()


@router.get("/{job_id}")
async def get_job(
    job_id: UUID,
    database: DatabaseDep = DatabaseDep,
) -> Job:
    jobs_repository = JobsRepository(database)
    job = await jobs_repository.read_one(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail=f"Job id={job_id} not found")
    return job


@router.delete("/{job_id}")
async def delete_job(
    job_id: UUID,
    database: DatabaseDep = DatabaseDep,
) -> None:
    jobs_repository = JobsRepository(database)
    await jobs_repository.delete(job_id)
    return None


@router.patch("/")
async def update_job(
    job: Job,
    database: DatabaseDep = DatabaseDep,
) -> Job:
    jobs_repository = JobsRepository(database)
    return await jobs_repository.update_partial(job)

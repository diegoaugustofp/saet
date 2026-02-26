"""Adapter de agendamento usando APScheduler.

Responsavel por disparar a execucao periodica das estrategias
conforme o timeframe configurado.
"""

from collections.abc import Callable, Coroutine
from typing import Any

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logger = structlog.get_logger()


class SchedulerAdapter:
    """Adapter para agendamento de execucao de estrategias usando APScheduler."""
    
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()
        self._jobs: dict[str, str] = {}
    
    def start(self) -> None:
        """Inicia o scheduler."""
        if not self._scheduler.running:
            self._scheduler.start()
            logger.info("scheduler_started")
    
    def stop(self) -> None:
        """Para o scheduler."""
        if self._scheduler.running:
            self._scheduler.shutdown(wait=False)
            logger.info("scheduler_stopped")
    
    def add_interval_job(
        self,
        job_id: str,
        func: Callable[..., Coroutine[Any, Any, Any]],
        minutes: int = 5,
        **kwargs: Any,
    ) -> None:
        """Adiciona um job com intervalo fixo.
        Args:
            job_id: Identificador unico do job.
            func: Funcao async a ser executada.
            minutes: Intervalo em minutos (padrao: 5, conforme SYS-NFR-001).
            **kwargs: Argumentos adicionais para a funcao.
        """
        
        self._scheduler.add_job(
            func,
            trigger=IntervalTrigger(minutes=minutes),
            id=job_id,
            replace_existing=True,
            kwargs=kwargs,
        )
        
        self._jobs[job_id] = f"interval:{minutes}m"
        logger.info("job_added", job_id=job_id, interval=f"{minutes}m")
    
    
    def add_cron_job(
        self,
        job_id: str,
        func: Callable[..., Coroutine[Any, Any, Any]],
        cron_expression: str,
        **kwargs: Any,
    ) -> None:
        """Adiciona um job com expressao cron.
        Args:
            job_id: Identificador unico do job.
            func: Funcao async a ser executada.
            cron_expression: Expressao cron (ex: '*/5 * * * *').
            **kwargs: Argumentos adicionais para a funcao.
        """
        
        parts = cron_expression.split()
        trigger = CronTrigger(
            minute=parts[0] if len(parts) > 0 else "*",
            hour=parts[1] if len(parts) > 1 else "*",
            day=parts[2] if len(parts) > 2 else "*",
            month=parts[3] if len(parts) > 3 else "*",
            day_of_week=parts[4] if len(parts) > 4 else "*",
        )
        
        self._scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            kwargs=kwargs,
        )
        
        self._jobs[job_id] = f"cron:{cron_expression}"
        
        logger.info("job_added", job_id=job_id, cron=cron_expression)
    
    
    def remove_job(self, job_id: str) -> None:
        """Remove um job agendado."""
        
        self._scheduler.remove_job(job_id)
        
        self._jobs.pop(job_id, None)
        
        logger.info("job_removed", job_id=job_id)
    
    def list_jobs(self) -> dict[str, str]:
        """Retorna todos os jobs agendados."""
        
        return dict(self._jobs)
    
    @property
    def is_running(self) -> bool:
        """Retorna se o scheduler esta em execucao."""
        
        return self._scheduler.running
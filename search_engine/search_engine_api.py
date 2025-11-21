from fastapi import FastAPI, Query
import uvicorn
from typing import List, Dict, Any
from contextlib import asynccontextmanager
from search_engine import SearchEngine
from tqdm import tqdm
import os

dataset_dir = './search_engine/corpus'

# 全局变量，用于存储 SearchEngine 实例
search_engine = None

# 使用 lifespan 上下文管理器替代 on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global search_engine
    print("Initializing SearchEngine...")
    search_engine = SearchEngine(dataset_dir, embed_model_name='vidore/colqwen2-v1.0')
    print("SearchEngine initialized successfully!")
    yield
    # Shutdown
    print("Shutting down SearchEngine...")

# 创建 FastAPI 应用实例
app = FastAPI(
    title="VRAG Search Engine API",
    description="Visual Retrieval-Augmented Generation Search Engine API using ColQwen2 embeddings.",
    version="1.0.0",
    lifespan=lifespan,
)


# 根路径 - 显示API信息
@app.get("/")
async def root():
    """API根路径，返回服务信息"""
    return {
        "service": "VRAG Search Engine API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/search": "POST/GET - Search images using text queries",
            "/docs": "GET - Interactive API documentation",
            "/redoc": "GET - ReDoc API documentation"
        },
        "example_usage": {
            "method": "GET",
            "url": "http://localhost:8002/search?queries=artificial%20intelligence&queries=machine%20learning",
            "description": "Search for images related to queries"
        }
    }

# 定义搜索 API 端点
@app.get(
    "/search",
    summary="Perform a search query.",
    description="Executes a search using the initialized SearchEngine and returns the results.",
    response_model=List[List[Dict[str, Any]]]
)
async def search(queries: List[str] = Query(..., description="List of search queries")):
    """
    执行搜索操作。

    Args:
        queries: 搜索查询字符串列表。

    Returns:
        搜索结果列表，每个查询返回Top-K相关图片。
    """
    results_batch = search_engine.batch_search(queries)
    results_batch = [[dict(idx=idx, image_file=os.path.join(f'./search_engine/corpus/img', file)) for idx, file in enumerate(query_results)] for query_results in results_batch]
    return results_batch

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

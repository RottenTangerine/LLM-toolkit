from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # DeepSeek 配置
    DS_ENDPOINT: str = Field(
        default="https://api.deepseek.com",
        description="DeepSeek API 服务端点",
        alias="DS_ENDPOINT"
    )
    DS_API_KEY: str = Field(
        ...,
        description="DeepSeek API 密钥（必填）",
        alias="DS_API_KEY"
    )
    DS_MODEL: str = Field(
        default="deepseek-chat",
        description="DeepSeek 模型名称",
        alias="DS_MODEL"
    )

    # Embedding 配置
    EMBEDDING_ENDPOINT: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings",
        description="Embedding 服务端点",
        alias="EMBEDDING_ENDPOINT"
    )
    EMBEDDING_API_KEY: str = Field(
        ...,
        description="Embedding API 密钥（必填）",
        alias="EMBEDDING_API_KEY"
    )
    EMBEDDING_MODEL: str = Field(
        default="text-embedding-v2",
        description="Embedding 模型名称",
        alias="EMBEDDING_MODEL"
    )

    class Config:
        env_file = ".env"  # 确保 .env 文件在项目根目录
        env_file_encoding = "utf-8"
        extra = "ignore"  # 忽略未定义的字段


settings = Settings()

if __name__ == '__main__':
    print("DeepSeek 配置:")
    print(f"Endpoint: {settings.DS_ENDPOINT}")
    print(f"Model: {settings.DS_MODEL}")

    print("\nEmbedding 配置:")
    print(f"Endpoint: {settings.EMBEDDING_ENDPOINT}")
    print(f"Model: {settings.EMBEDDING_MODEL}")
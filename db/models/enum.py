class KnowledgeSource:
    """文件来源"""

    CREATE = "create"
    FILE = "file"


class ReleaseStatus:
    """发布状态"""

    PARSING = "parsing"  # 解析中
    PARSE_SUCCEED = "parse_succeed"  # 解析完成
    PARSE_FAILED = "parse_failed" # 解析失败
    QA_GENERATING = "qa_generating"  # 自动生成QA中
    QA_AWAIT = "qa_await"  # QA待发布
    QA_RELEASED = "qa_released"  # QA已发布
    QA_GENERATED_FAILED = "qa_generated_failed"  # 自动生成QA失败
    # AWAIT = "await"
    # RELEASED = "released"
    # LEARNING = "learning"


class UploadStatus:
    """上传状态"""

    UPLOADING = "uploading"
    SUCCESS = "success"
    FAIL = "fail"


class DocumentType:
    """文件类型"""

    WORD = "word"
    PPT = "ppt"
    PDF = "pdf"
    EXCEL = "excel"
    QA = "qa"
    
class FileSource:
    """document表任务类型"""
    KnowledgeQA = "knowledge" # 知识问答
    Document = "document" # 文件解析 默认是文件解析
    
class Source:
    """knowledge表任务类型"""
    FILE = "file" # 文件解析
    CREATE = "create" # 知识问答，默认是知识问答

class GradeScore:
    """等级分数"""
    YES = "是"
    NO = "否"

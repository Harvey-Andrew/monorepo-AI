"""
工程化脚本 - 类型生成

读取 backend/apps 中的 Pydantic 模型，生成 TypeScript 类型定义
"""

import os
import sys
import ast
import re
from pathlib import Path
from typing import Dict, List, Set


def extract_pydantic_models(file_path: Path) -> Dict[str, Dict]:
    """从 Python 文件中提取 Pydantic 模型"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    models = {}

    # 使用 AST 解析
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return models

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # 检查是否继承自 BaseModel
            for base in node.bases:
                base_name = ""
                if isinstance(base, ast.Name):
                    base_name = base.id
                elif isinstance(base, ast.Attribute):
                    base_name = base.attr

                if "Model" in base_name or "Response" in base_name:
                    fields = {}
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(
                            item.target, ast.Name
                        ):
                            field_name = item.target.id
                            field_type = ast.unparse(item.annotation)
                            fields[field_name] = field_type
                    models[node.name] = fields

    return models


def python_type_to_ts(py_type: str) -> str:
    """Python 类型转 TypeScript 类型"""
    # 清理类型字符串
    py_type = py_type.strip()

    # 基本类型映射
    type_map = {
        "str": "string",
        "int": "number",
        "float": "number",
        "bool": "boolean",
        "None": "null",
        "Any": "any",
    }

    # 直接映射
    if py_type in type_map:
        return type_map[py_type]

    # List[X] -> X[]
    list_match = re.match(r"List\[(.+)\]", py_type)
    if list_match:
        inner = python_type_to_ts(list_match.group(1))
        return f"{inner}[]"

    # Optional[X] -> X | null
    optional_match = re.match(r"Optional\[(.+)\]", py_type)
    if optional_match:
        inner = python_type_to_ts(optional_match.group(1))
        return f"{inner} | null"

    # 其他类型保持原样
    return py_type


def generate_ts_interface(name: str, fields: Dict[str, str]) -> str:
    """生成 TypeScript 接口"""
    lines = [f"export interface {name} {{"]
    for field_name, field_type in fields.items():
        ts_type = python_type_to_ts(field_type)
        lines.append(f"  {field_name}: {ts_type};")
    lines.append("}")
    return "\n".join(lines)


def main():
    """主函数"""
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    # 后端 schemas 目录
    apps_dir = root_dir / "backend" / "apps"

    # 前端类型输出目录
    output_dir = root_dir / "frontend" / "types" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_interfaces: List[str] = []
    all_interfaces.append("// 自动生成的 API 类型定义")
    all_interfaces.append("// 由 scripts/gen_types.py 生成")
    all_interfaces.append("")

    # 遍历所有 schemas.py
    if apps_dir.exists():
        for app_dir in sorted(apps_dir.iterdir()):
            if not app_dir.is_dir():
                continue

            schemas_file = app_dir / "schemas.py"
            if schemas_file.exists():
                models = extract_pydantic_models(schemas_file)
                if models:
                    all_interfaces.append(f"// === {app_dir.name} ===")
                    for name, fields in models.items():
                        all_interfaces.append(generate_ts_interface(name, fields))
                    all_interfaces.append("")

    # 写入文件
    output_file = output_dir / "api.d.ts"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_interfaces))

    print(f"类型定义已生成: {output_file}")


if __name__ == "__main__":
    main()

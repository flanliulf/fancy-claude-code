#!/usr/bin/env python3
"""
java-spring-boot 技能的校验脚本。
分类：通用
"""

import os
import sys
import yaml
import json
from pathlib import Path


def validate_config(config_path: str) -> dict:
    """
    校验技能配置文件。

    Args:
        config_path: config.yaml 的文件路径

    Returns:
        dict: 包含 'valid' 和 'errors' 键的校验结果
    """
    errors = []

    if not os.path.exists(config_path):
        return {"valid": False, "errors": ["Config file not found"]}

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return {"valid": False, "errors": [f"YAML parse error: {e}"]}

    # 校验必填字段
    if 'skill' not in config:
        errors.append("Missing 'skill' section")
    else:
        if 'name' not in config['skill']:
            errors.append("Missing skill.name")
        if 'version' not in config['skill']:
            errors.append("Missing skill.version")

    # 校验设置项
    if 'settings' in config:
        settings = config['settings']
        if 'log_level' in settings:
            valid_levels = ['debug', 'info', 'warn', 'error']
            if settings['log_level'] not in valid_levels:
                errors.append(f"Invalid log_level: {settings['log_level']}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "config": config if not errors else None
    }


def validate_skill_structure(skill_path: str) -> dict:
    """
    校验技能目录结构。

    Args:
        skill_path: 技能目录的路径

    Returns:
        dict: 目录结构校验结果
    """
    required_dirs = ['assets', 'scripts', 'references']
    required_files = ['SKILL.md']

    errors = []

    # 检查必需文件
    for file in required_files:
        if not os.path.exists(os.path.join(skill_path, file)):
            errors.append(f"Missing required file: {file}")

    # 检查必需目录
    for dir in required_dirs:
        dir_path = os.path.join(skill_path, dir)
        if not os.path.isdir(dir_path):
            errors.append(f"Missing required directory: {dir}/")
        else:
            # 检查目录是否有实际内容（不只是 .gitkeep）
            files = [f for f in os.listdir(dir_path) if f != '.gitkeep']
            if not files:
                errors.append(f"Directory {dir}/ has no real content")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "skill_name": os.path.basename(skill_path)
    }


def main():
    """主校验入口。"""
    skill_path = Path(__file__).parent.parent

    print(f"正在校验 java-spring-boot 技能...")
    print(f"路径：{skill_path}")

    # 校验目录结构
    structure_result = validate_skill_structure(str(skill_path))
    print(f"\n目录结构校验：{'通过' if structure_result['valid'] else '失败'}")
    if structure_result['errors']:
        for error in structure_result['errors']:
            print(f"  - {error}")

    # 校验配置
    config_path = skill_path / 'assets' / 'config.yaml'
    if config_path.exists():
        config_result = validate_config(str(config_path))
        print(f"\n配置校验：{'通过' if config_result['valid'] else '失败'}")
        if config_result['errors']:
            for error in config_result['errors']:
                print(f"  - {error}")
    else:
        print("\n配置校验：已跳过（未找到 config.yaml）")

    # 汇总结果
    all_valid = structure_result['valid']
    print(f"\n==================================================")
    print(f"总体结果：{'有效' if all_valid else '无效'}")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())

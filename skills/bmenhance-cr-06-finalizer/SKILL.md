---
name: bmenhance-cr-06-finalizer
description: "Update Story status to Done and sync workflow tracking documents after CR approval. Use when user mentions 'CR done', 'CR approved', 'CR complete', 'story done', 'mark done', 'close story', 'CR 完成', 'CR 通过', '标记完成', '关闭 Story', 'Story 完成', '更新状态为 Done', 'CR 收尾', or wants to finalize a Story after code review approval. Capable of updating Story status, sprint-status.yaml, and bmm-workflow-status.yaml in one atomic operation."
allowed-tools: Read, Edit, Grep, Glob
metadata:
  version: "1.1.1"
---

[技能说明]
    Story 通过代码审查（CR Approved）后的收尾操作技能。一次性完成 Story 状态更新和流程文档同步，确保所有跟踪文件的状态一致性。是 bmenhance CR 工作流的最终环节（承接 bmenhance-cr-01 ~ 05 之后）。

[核心能力]
    - **CR 审批确认**：读取最新一轮 CR 评估文件，验证 CR 结论确实为 Approved
    - **Story 状态更新**：将 Story 文件中的状态字段更新为 Done
    - **Sprint 状态同步**：更新 `_bmad-output/implementation-artifacts/sprint-status.yaml` 中对应 Story 的状态
    - **工作流状态同步**：更新 `_bmad-output/planning-artifacts/bmm-workflow-status.yaml` 中对应 Story 的状态
    - **Epic 状态联动**：检测所属 Epic 下所有 Story 是否均已 Done，如果是则提示用户是否同步更新 Epic 状态
    - **防重复执行**：检测 Story 是否已经是 Done 状态，避免重复操作
    - **操作审计**：输出完整的状态变更清单供用户确认

[执行流程]
    路径约定和文件名格式以 `references/cr-config.md` 为准。

    Step 1：定位 Story 和 CR 审查目录
        - 接收用户指定的 Story 标识（Story 文件路径或 Story ID）
        - 读取 `references/cr-config.md` 获取路径约定
        - 按配置中的 Story 文件目录定位 Story 文件
        - 按配置中的 Story ID 规则提取 `{story-id}`
        - 按配置中的代码审查目录格式确定路径
        - 生成数据：story-id、story-file-path、code-review-dir

    Step 2：验证 CR 审批状态
        - 按配置中的审查评估文件名格式，扫描 code-review-dir 下匹配的文件
        - 找到 round 值最大的评估文件
        - 读取该文件，确认 CR 结论为 Approved（查找"Approved"、"通过"等关键词）
        - IF CR 结论不是 Approved：
            - 立即停止，告知用户："❌ 最新一轮 CR 评估结论不是 Approved，无法标记为 Done"
            - 展示实际的 CR 结论内容
            - 退出流程
        - IF 找不到评估文件：
            - 立即停止，告知用户："❌ 未找到 CR 评估文件，请先完成代码审查流程"
            - 退出流程
        - 生成数据：cr-conclusion（CR 结论）、latest-evaluation-file

    Step 3：检查当前状态（防重复）
        - 读取 Story 文件，检查当前状态字段
        - IF 状态已经是 Done：
            - 告知用户："ℹ️ Story {story-id} 已经是 Done 状态，无需重复操作"
            - 退出流程
        - 生成数据：current-status

    Step 4：更新 Story 文件状态
        - 在 Story 文件中找到状态字段（如 `status:` 行）
        - 将状态值更新为 `done`
        - 生成数据：story-updated

    Step 5：更新 sprint-status.yaml
        - 按 `references/cr-config.md` 中的实现产物目录配置定位 sprint-status.yaml
        - IF 文件不存在：
            - 警告用户："⚠️ sprint-status.yaml 不存在，跳过此步骤"
            - 跳到 Step 6
        - 在 `development_status` 段中找到匹配当前 Story 的条目（通过 story-id 前缀匹配）
        - 将该条目的状态值更新为 `done`
        - 更新 `last_updated` 时间戳为当前时间（格式：YYYY-MM-DD HH:MM）
        - 生成数据：sprint-status-updated

    Step 6：更新 bmm-workflow-status.yaml
        - 按 `references/cr-config.md` 中的规划产物目录配置定位 bmm-workflow-status.yaml
        - IF 文件不存在：
            - 警告用户："⚠️ bmm-workflow-status.yaml 不存在，跳过此步骤"
            - 跳到 Step 7
        - 找到匹配当前 Story 的条目
        - 将该条目的状态值更新为 `done`
        - 更新文件的时间戳字段为当前时间
        - 生成数据：workflow-status-updated

    Step 7：检测 Epic 完成状态
        - 从 story-id 中提取 epic 编号（如 story-id 为 1-2，则 epic 编号为 1）
        - 在 sprint-status.yaml 的 `development_status` 中查找所有以该 epic 编号开头的 Story 条目
        - 检查这些 Story 是否全部为 `done` 状态
        - IF 全部 Done：
            - 提示用户："🎉 Epic {epic-num} 下所有 Story 已全部完成！是否将 Epic 状态也更新为 done？"
            - 等待用户确认后再执行 Epic 状态更新
        - IF 未全部 Done：
            - 展示剩余未完成的 Story 列表

    Step 8：输出变更总结
        - 展示完整的操作清单：
            ```
            ✅ CR Done 收尾操作完成！

            📋 变更清单：
            - Story 文件：{story-file-path} → status: done
            - sprint-status.yaml：{story-key} → done
            - bmm-workflow-status.yaml：{story-key} → done
            - Epic 状态：{epic-status-info}

            📌 CR 信息：
            - 最终 CR 轮次：Round {n}
            - CR 结论：Approved
            - 评估文件：{latest-evaluation-file}
            ```
        - 完成后返回："✅ Story {story-id} 已标记为 Done，所有流程文档已同步更新"

[注意事项]
    - **前置条件**：必须确认最新一轮 CR 评估结论为 Approved 才能执行，不允许跳过 CR 验证
    - **状态只进不退**：Story 状态只允许从 review/in-progress 变更为 done，禁止将已 done 的 Story 改回其他状态
    - **文件容错**：sprint-status.yaml 或 bmm-workflow-status.yaml 不存在时跳过对应步骤并警告，不阻塞整体流程
    - **Epic 状态需确认**：Epic 状态变更必须由用户显式确认，不自动更新
    - 路径约定和文件名格式以 `references/cr-config.md` 为准，不硬编码
    - 始终使用中文输出
    - 如果 Story 文件中没有明确的 status 字段，根据文件内容和格式智能定位状态标记位置
    - 本 Skill 不修改任何源代码文件，只更新状态跟踪文档

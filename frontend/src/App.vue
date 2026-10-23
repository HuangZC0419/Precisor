<template>
  <div class="app-shell" :class="{ 'theme-dark': isDarkMode }">
    <aside class="app-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-brand" role="button" tabindex="0" :aria-label="sidebarCollapsed ? '展开侧边栏' : '折叠侧边栏'" aria-expanded="true" @click="sidebarCollapsed = !sidebarCollapsed" @keydown.enter="sidebarCollapsed = !sidebarCollapsed" @keydown.space.prevent="sidebarCollapsed = !sidebarCollapsed">
        <div class="brand-icon">
          <svg viewBox="0 0 32 32" fill="none">
            <rect x="2" y="2" width="28" height="28" rx="8" stroke="currentColor" stroke-width="2" />
            <path d="M10 12h12M10 17h8M10 22h10" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <circle cx="24" cy="12" r="2" fill="currentColor" />
          </svg>
        </div>
        <span class="brand-text">Precisor</span>
      </div>

      <div class="sidebar-history-container" :class="{ hidden: sidebarCollapsed }">
        <div class="sidebar-history-header">
          <span>历史记录</span>
          <button class="btn-refresh-history" @click.stop="fetchHistory" title="刷新历史记录">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" :class="{ spin: isHistoryLoading }">
              <polyline points="23 4 23 10 17 10" />
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
            </svg>
          </button>
        </div>

        <button class="btn-new-task-sidebar" @click.stop="reset">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
            <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          <span>新建任务</span>
        </button>

        <div class="sidebar-history-list">
          <div v-if="isHistoryLoading && historyRecords.length === 0" class="history-empty">
            加载中...
          </div>
          <div v-else-if="historyRecords.length === 0" class="history-empty">
            暂无历史记录
          </div>
          <div 
            v-else
            v-for="record in historyRecords" 
            :key="record.task_id" 
            class="history-item"
            :class="{ active: taskInfo.task_id === record.task_id }"
            @click="loadHistoryTask(record)"
          >
            <div class="history-item-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="16" height="16">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              </svg>
            </div>
            <div class="history-item-content">
              <div class="history-item-title" :title="record.file_name">{{ record.file_name }}</div>
              <div class="history-item-meta">
                <span class="history-item-time">{{ formatDate(record.created_at) }}</span>
                <span class="history-item-status" :class="record.status">
                  {{ record.status === 'completed' ? '已完成' : record.status === 'failed' ? '失败' : '处理中' }}
                </span>
              </div>
            </div>
            <button
              class="history-item-delete"
              @click.stop="pendingDeleteId = record.task_id"
              title="删除此记录"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 模型管理入口按钮 -->
      <button class="nav-item nav-item-models" :class="{ active: currentPage === 'models' }" @click="currentPage = 'models'; wizardStep = 1" title="模型管理">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5" />
          <path d="M2 12l10 5 10-5" />
        </svg>
        <span class="nav-label">模型管理</span>
      </button>

      <div class="sidebar-footer">
        <button class="nav-item" @click="isDarkMode = !isDarkMode" :title="isDarkMode ? '切换浅色' : '切换深色'">
          <svg v-if="!isDarkMode" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
          <span class="nav-label">{{ isDarkMode ? '浅色模式' : '深色模式' }}</span>
        </button>
        <div class="sidebar-version">v1.2.0</div>
      </div>
    </aside>

    <div class="app-main-wrap">
      <header class="app-header">
        <div class="header-left">
          <button class="header-menu-btn" @click="sidebarCollapsed = !sidebarCollapsed" :title="sidebarCollapsed ? '展开侧边栏' : '折叠侧边栏'" aria-label="切换侧边栏">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
          <div class="header-breadcrumb">
            <button class="breadcrumb-tab" :class="{ active: currentPage === 'console' }" @click="currentPage = 'console'">系统控制台</button>
            <button class="breadcrumb-tab" :class="{ active: currentPage === 'models' }" @click="currentPage = 'models'">模型管理</button>
          </div>
        </div>
        <div class="header-right">
          <div v-if="taskInfo.task_id" class="header-task-id">
            <span class="task-id-label">任务</span>
            <code class="task-id-value">{{ taskInfo.file_name }}</code>
          </div>
          <div class="header-status-pill" :class="taskInfo.status">
            <span class="status-dot"></span>
            <span>{{ statusText }}</span>
          </div>
        </div>
      </header>

      <!-- Wizard Bar -->
      <div v-if="currentPage === 'console'" class="wizard-bar">
        <div
          v-for="(step, idx) in wizardSteps"
          :key="step.key"
          class="wizard-step"
          :class="{
            active: wizardStep === idx + 1,
            done: wizardStep > idx + 1
          }"
        >
          <div class="wstep-circle">
            <svg v-if="wizardStep > idx + 1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" width="14" height="14">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            <span v-else>{{ idx + 1 }}</span>
          </div>
          <span class="wstep-label">{{ step.label }}</span>
          <div v-if="idx < wizardSteps.length - 1" class="wstep-connector">
            <div class="wstep-connector-fill" :style="{ width: wizardStep > idx + 1 ? '100%' : '0%' }"></div>
          </div>
        </div>
      </div>

      <main class="app-main" v-if="currentPage === 'console'">
        <!-- Step 1-5 content unchanged -->

        <!-- Step 1: Upload -->
        <section v-if="wizardStep === 1" class="step-view step-upload">
          <div class="step-hero">
            <h2 class="step-title">上传文档</h2>
            <p class="step-desc">支持 PDF、PNG、JPG 格式，拖拽或点击选择文件，最大 50MB</p>
          </div>
          <div class="upload-center">
            <div
              class="drop-zone"
              :class="{ 'drag-over': isDragOver, 'has-file': selectedFile }"
              @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false"
              @drop.prevent="onDrop"
              @click="!selectedFile && openFilePicker()"
            >
              <transition name="fade-scale" mode="out-in">
                <div v-if="!selectedFile" key="empty" class="drop-zone-inner">
                  <div class="drop-icon-ring">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="17 8 12 3 7 8" />
                      <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                  </div>
                  <p class="drop-title">拖拽文件到此处</p>
                  <p class="drop-subtitle">或点击选择文件</p>
                  <div class="drop-formats">
                    <span class="format-badge">PDF</span>
                    <span class="format-badge">PNG</span>
                    <span class="format-badge">JPG</span>
                  </div>
                  <p class="drop-hint">最大 50MB</p>
                </div>
                <div v-else key="file" class="drop-zone-file-preview">
                  <div class="file-preview-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                    </svg>
                  </div>
                  <p class="drop-file-name">{{ selectedFile.name }}</p>
                  <p class="drop-file-size">{{ formatSize(selectedFile.size) }}</p>
                  <button class="drop-file-remove" @click.stop="clearFile" title="移除文件">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                  </button>
                </div>
              </transition>
            </div>
            <input ref="fileInput" type="file" class="hidden-input" accept=".pdf,.png,.jpg,.jpeg" @change="handleFileChange" />
            <button class="btn-primary btn-next" :disabled="!selectedFile" @click="wizardStep = 2">
              下一步：配置参数
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="18" height="18">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </button>
          </div>
        </section>

        <!-- Step 2: Configure -->
        <section v-else-if="wizardStep === 2" class="step-view step-config">
          <div class="step-hero">
            <h2 class="step-title">配置解析参数</h2>
            <p class="step-desc">选择后端引擎、语言策略与功能开关，完成后点击开始解析</p>
          </div>
          <div class="config-layout">
            <div class="config-card card-glass">
              <div class="config-section">
                <h4 class="config-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <rect x="2" y="3" width="20" height="14" rx="2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" />
                  </svg>
                  后端引擎
                </h4>
                <div class="radio-grid">
                  <label
                    v-for="item in availableOptions.backend_types"
                    :key="item.value"
                    class="radio-card"
                    :class="{ active: parseConfig.backend_type === item.value }"
                  >
                    <input v-model="parseConfig.backend_type" type="radio" :value="item.value" />
                    <div class="radio-content">
                      <span class="radio-title">{{ item.label }}</span>
                      <span class="radio-desc">{{ item.description }}</span>
                    </div>
                    <div class="radio-check" v-if="parseConfig.backend_type === item.value">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" width="14" height="14">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </div>
                  </label>
                </div>
              </div>

              <div class="config-row">
                <div class="config-section config-half">
                  <h4 class="config-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <circle cx="12" cy="12" r="10" /><path d="M2 12h20" />
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                    </svg>
                    语言
                  </h4>
                  <select v-model="parseConfig.language" class="select-field">
                    <option v-for="item in availableOptions.languages" :key="item.value" :value="item.value">{{ item.label }}</option>
                  </select>
                </div>
                <div class="config-section config-half">
                  <h4 class="config-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <rect x="2" y="2" width="20" height="20" rx="2.18" />
                      <line x1="7" y1="2" x2="7" y2="22" /><line x1="17" y1="2" x2="17" y2="22" /><line x1="2" y1="12" x2="22" y2="12" />
                    </svg>
                    OCR 模式
                  </h4>
                  <select v-model="parseConfig.ocr_mode" class="select-field">
                    <option v-for="item in availableOptions.ocr_modes" :key="item.value" :value="item.value">{{ item.label }}</option>
                  </select>
                </div>
              </div>

              <div class="config-section">
                <h4 class="config-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" />
                    <rect x="14" y="14" width="7" height="7" /><rect x="3" y="14" width="7" height="7" />
                  </svg>
                  功能开关
                </h4>
                <div class="toggle-grid">
                  <label v-for="item in availableOptions.feature_toggles" :key="item.key" class="toggle-card">
                    <div class="toggle-content">
                      <span class="toggle-title">{{ item.label }}</span>
                      <span class="toggle-desc">{{ item.description }}</span>
                    </div>
                    <div class="toggle-switch-wrap">
                      <input v-model="parseConfig[item.key]" type="checkbox" class="toggle-switch" />
                      <span class="toggle-track"></span>
                    </div>
                  </label>
                </div>
              </div>

              <div class="config-preview">
                <div class="preview-header">
                  <span class="preview-label">当前参数预览</span>
                  <span class="preview-count">{{ configPreviewTags.length }} 项</span>
                </div>
                <div class="preview-tags">
                  <span v-for="tag in configPreviewTags" :key="tag" class="preview-tag">{{ tag }}</span>
                </div>
              </div>

              <div class="config-actions">
                <button class="btn-secondary" @click="wizardStep = 1">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                    <polyline points="15 18 9 12 15 6" />
                  </svg>
                  上一步
                </button>
                <button class="btn-primary btn-start" :disabled="isUploading" @click="uploadFile">
                  <svg v-if="!isUploading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18" class="spin">
                    <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                    <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                  </svg>
                  {{ isUploading ? '上传中...' : '开始解析' }}
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Step 3: Processing -->
        <section v-else-if="wizardStep === 3" class="step-view step-processing" aria-live="polite" aria-label="文档解析进度">
          <div class="processing-card card-glass">
            <div class="processing-header">
              <div class="processing-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32" class="spin">
                  <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                  <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                </svg>
              </div>
              <div>
                <h2>正在解析文档</h2>
                <p class="processing-filename">{{ taskInfo.file_name }}</p>
              </div>
            </div>

            <div class="feature-tags-row">
              <span v-for="tag in taskInfo.feature_summary || []" :key="tag" class="feature-tag">{{ tag }}</span>
            </div>

            <div class="stepper">
              <div
                v-for="(stage, idx) in stages"
                :key="stage.label"
                class="step"
                :class="{ active: idx === currentStage, done: idx < currentStage }"
              >
                <div class="step-circle">
                  <svg v-if="idx < currentStage" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" width="14" height="14">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                  <span v-else>{{ idx + 1 }}</span>
                </div>
                <span class="step-label">{{ stage.label }}</span>
              </div>
            </div>

            <div class="progress-section">
              <div class="progress-bar-wrap">
                <div class="progress-bubble" :style="{ left: `clamp(20px, ${taskInfo.progress}%, calc(100% - 20px))` }">
                  <span>{{ taskInfo.progress }}%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: `${taskInfo.progress}%` }">
                    <div class="progress-shine"></div>
                  </div>
                </div>
              </div>
            </div>

            <div class="processing-stats">
              <div class="stat-item">
                <span class="stat-value">{{ formatDuration(elapsed) }}</span>
                <span class="stat-label">已用时间</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-value">{{ taskInfo.progress }}%</span>
                <span class="stat-label">完成进度</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-value">{{ estimatedRemaining }}</span>
                <span class="stat-label">预计剩余</span>
              </div>
            </div>
            <div class="processing-message">
              <div class="processing-stage">{{ taskInfo.stage_label || stages[currentStage].label }}</div>
              <p>{{ taskInfo.message || '正在处理中...' }}</p>
            </div>
          </div>
        </section>

        <!-- Step 4: Results -->
        <section v-else-if="wizardStep === 4" class="step-view step-results">
          <div class="result-top-bar">
            <div class="result-info">
              <h2 class="result-filename">{{ taskInfo.file_name || selectedFile?.name || '解析结果' }}</h2>
              <div class="result-params">
                <span v-for="tag in taskInfo.feature_summary || []" :key="tag" class="param-badge">{{ tag }}</span>
              </div>
            </div>
          </div>

            <div class="toolbar">
              <div class="toolbar-left">
                <div class="tool-group">
                  <button class="tool-btn" :class="{ active: splitMode === 'horizontal' }" @click="splitMode = 'horizontal'" title="左右分栏" aria-label="左右分栏布局">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <rect x="3" y="3" width="8" height="18" rx="1" /><rect x="13" y="3" width="8" height="18" rx="1" />
                    </svg>
                  </button>
                  <button class="tool-btn" :class="{ active: splitMode === 'vertical' }" @click="splitMode = 'vertical'" title="上下分栏" aria-label="上下分栏布局">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <rect x="3" y="3" width="18" height="8" rx="1" /><rect x="3" y="13" width="18" height="8" rx="1" />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="toolbar-right">
                <button class="tool-btn" :class="{ active: pdfFullscreen }" @click="pdfFullscreen = !pdfFullscreen" title="PDF 全屏">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <polyline points="15 3 21 3 21 9" /><polyline points="9 21 3 21 3 15" />
                    <line x1="21" y1="3" x2="14" y2="10" /><line x1="3" y1="21" x2="10" y2="14" />
                  </svg>
                </button>
                <button class="tool-btn" :class="{ active: mdFullscreen }" @click="mdFullscreen = !mdFullscreen" title="Markdown 全屏">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                  </svg>
                </button>
                <button class="tool-btn" @click="copyMarkdown" title="复制 Markdown">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <rect x="9" y="9" width="13" height="13" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                  </svg>
                </button>
                <template v-if="isEditing">
                  <button class="tool-btn btn-save" :disabled="isSaving" @click="saveEdit" title="保存修改">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
                      <polyline points="17 21 17 13 7 13 7 21" /><polyline points="7 3 7 8 15 8" />
                    </svg>
                  </button>
                  <button class="tool-btn btn-cancel-edit" @click="cancelEdit" title="取消编辑">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                  </button>
                </template>
                <button v-else class="tool-btn btn-edit" @click="startEdit" title="编辑 Markdown">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                  </svg>
                </button>
                <span class="tool-sep"></span>
                <button class="btn-primary btn-mark-cta" :disabled="taskInfo.status !== 'completed'" @click="navigateToStep(5)" title="进入快速标注">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <path d="M5 4h10l4 4v12H5z" />
                    <path d="M9 12h6M9 16h4M15 4v4h4" />
                  </svg>
                  <span>快速标注</span>
                </button>
              </div>
            </div>

            <div
              class="panels-container"
              :class="[splitMode, { 'pdf-fullscreen': pdfFullscreen, 'md-fullscreen': mdFullscreen }]"
            >
              <div v-show="!mdFullscreen" class="panel panel-pdf">
                <div class="panel-header" @dblclick="pdfFullscreen = !pdfFullscreen">
                  <div class="panel-header-left">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                    </svg>
                    <span>Layout PDF</span>
                  </div>
                  <div class="panel-header-right">
                    <span v-if="pdfLoadError" class="pdf-status-error">加载失败</span>
                    <span v-else-if="pdfLoading" class="pdf-status-loading">加载中...</span>
                    <span class="panel-hint">双击全屏</span>
                  </div>
                </div>
                <div class="panel-body" :class="{ 'has-error': pdfLoadError }">
                  <div v-if="pdfLoadError" class="panel-error-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="12" y1="8" x2="12" y2="12" />
                      <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    <p class="panel-error-title">PDF 无法加载</p>
                    <p class="panel-error-desc">后端尚未生成布局 PDF 文件，请确认 Precisor 处理已完成。</p>
                    <button class="btn-retry" @click="retryLoadPdf">重新加载</button>
                  </div>
                  <iframe v-else :src="pdfUrl" class="pdf-iframe" frameborder="0" @load="onPdfLoad" @error="onPdfError"></iframe>
                </div>
              </div>

              <div v-show="!pdfFullscreen && !mdFullscreen" class="panel-divider" @mousedown="startResize">
                <div class="divider-handle"></div>
              </div>

              <div v-show="!pdfFullscreen" class="panel panel-md">
                <div class="panel-header" @dblclick="mdFullscreen = !mdFullscreen">
                  <div class="panel-header-left">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                      <line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
                    </svg>
                    <span>Markdown 结果</span>
                  </div>
                  <div class="panel-header-right">
                    <span class="word-count">{{ wordCount }} 字</span>
                    <span class="panel-hint">双击全屏</span>
                  </div>
                </div>
                <div class="panel-body md-body" ref="mdBodyRef">
                  <div v-if="mdLoadError" class="panel-error-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="12" y1="8" x2="12" y2="12" />
                      <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    <p class="panel-error-title">Markdown 加载失败</p>
                    <p class="panel-error-desc">无法获取解析结果，请检查后端服务是否正常运行。</p>
                    <button class="btn-retry" @click="retryLoadMd">重新加载</button>
                  </div>
                  <div v-else-if="mdLoading" class="panel-loading-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32" class="spin">
                      <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                      <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                    </svg>
                    <p>正在加载解析结果...</p>
                  </div>
                  <div v-else class="md-content-wrap review-md-content">
                    <div
                      :key="mdViewKey"
                      v-html="renderedMarkdown"
                      :contenteditable="isEditing"
                      ref="editableRef"
                      spellcheck="false"
                      :class="{ 'md-editing': isEditing }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

        </section>

        <!-- Step 5: Quick Annotation -->
        <section v-else-if="wizardStep === 5" class="step-view step-annotation">
          <div class="annotation-workspace-toolbar">
            <div class="annotation-workspace-copy">
              <div class="annotation-workspace-kicker">快速标注</div>
              <div class="annotation-workspace-status-row">
                <span class="annotation-status-pill">{{ annotationUpdatedText }}</span>
                <span class="annotation-workspace-tip">仅分析最近保存的 Markdown，不显示 PDF</span>
              </div>
            </div>
            <div class="annotation-workspace-actions">
              <button class="tool-btn" @click="copyMarkdown" title="复制 Markdown">
                复制 MD
              </button>
            </div>
          </div>

          <div class="annotation-workspace-body">
            <aside class="annotation-sidebar">
              <div class="annotation-card">
                <div class="annotation-card-tabs">
                  <button class="annotation-card-tab" :class="{ active: annotationMode === 'rules' }" @click="annotationMode = 'rules'">规则标注</button>
                  <button class="annotation-card-tab" :class="{ active: annotationMode === 'model' }" @click="annotationMode = 'model'; fetchSavedModels()">模型标注</button>
                </div>
                <div v-if="annotationMode === 'rules'">
                <div class="annotation-card-header">
                  <div>
                    <div class="annotation-title">标注规则</div>
                    <p class="annotation-desc">勾选规则后点击启动标注，使用导航浏览命中片段。</p>
                  </div>
                </div>

                <div class="annotation-utility-row">
                  <button class="annotation-utility-btn" @click="selectAllAnnotationRules">全选规则</button>
                  <button class="annotation-utility-btn" @click="clearAnnotationRules">清空选择</button>
                </div>

                <div class="annotation-settings-section">
                  <button class="annotation-settings-toggle" @click="annotationSettingsExpanded = !annotationSettingsExpanded">
                    <svg class="annotation-settings-chevron" :class="{ expanded: annotationSettingsExpanded }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <polyline points="9 18 15 12 9 6" />
                    </svg>
                    <span>规则标注参数设置</span>
                  </button>
                  <div v-show="annotationSettingsExpanded" class="annotation-rule-list">
                    <label v-for="rule in annotationRules" :key="rule.id" class="annotation-rule-item">
                      <input v-model="selectedAnnotationRules" type="checkbox" :value="rule.id" />
                      <div class="annotation-rule-content">
                        <div class="annotation-rule-top">
                          <span class="annotation-rule-label">{{ rule.label }}</span>
                          <span class="annotation-rule-count">{{ getRuleCount(rule.id) }}</span>
                        </div>
                        <p class="annotation-rule-desc">{{ rule.description }}</p>
                      </div>
                    </label>
                  </div>
                </div>

                <button
                  class="btn-start-annotation"
                  :disabled="annotationLoading || !selectedAnnotationRules.length"
                  @click="fetchAnnotations"
                >
                  <svg v-if="annotationLoading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" class="spin">
                    <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                    <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  <span>{{ annotationLoading ? '标注中...' : '启动标注' }}</span>
                </button>

                <div v-if="annotationLoading" class="annotation-empty-state">
                  正在分析 Markdown 中的有效信息...
                </div>
                <div v-else-if="annotationError" class="annotation-empty-state error">
                  {{ annotationError }}
                </div>
                <div v-else-if="!annotationLastRunAt && !annotationSnippets.length" class="annotation-empty-state">
                  请选择规则后点击「启动标注」。
                </div>
                <div v-else-if="annotationLastRunAt && !annotationSnippets.length" class="annotation-empty-state">
                  当前规则下暂无明显命中内容。
                </div>
                </div>

                <!-- Model Annotation Panel -->
                <div v-else-if="annotationMode === 'model'" class="annotation-model-panel">
                  <div class="annotation-model-section">
                    <label class="annotation-model-label">持久模型</label>
                    <select v-model="selectedPersistentModelId" class="select-field">
                      <option value="">-- 选择已训练模型 --</option>
                      <option v-for="m in savedModels" :key="m.model_id" :value="m.model_id">{{ m.model_name }} ({{ (m.entity_labels || m.labels || []).length }} 标签)</option>
                    </select>
                  </div>
                  <!-- 置信度控件：选择模型后即可见，标注前即可调整阈值 -->
                  <div class="conf-slider-card" v-if="selectedPersistentModelId">
                    <div class="conf-slider-card-header">
                      <span class="conf-slider-card-title">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                          <path d="M12 2L2 7l10 5 10-5-10-5z" /><path d="M2 17l10 5 10-5" /><path d="M2 12l10 5 10-5" />
                        </svg>
                        置信度阈值
                      </span>
                      <span class="conf-slider-badge" :class="{ 'conf-badge-high': modelConfThreshold >= 70, 'conf-badge-mid': modelConfThreshold >= 40, 'conf-badge-low': modelConfThreshold < 40 }">≥ {{ modelConfThreshold }}%</span>
                    </div>
                    <div class="conf-slider-track-wrap">
                      <div class="conf-slider-gradient" :style="{ '--conf-pct': modelConfThreshold + '%' }">
                        <div class="conf-slider-gradient-fill"></div>
                      </div>
                      <input type="range" v-model.number="modelConfThreshold" min="0" max="100" step="5" class="conf-slider" />
                    </div>
                    <div class="conf-slider-presets">
                      <button v-for="pct in [25, 50, 70, 90]" :key="pct" class="conf-preset-btn" :class="{ active: modelConfThreshold === pct }" @click="modelConfThreshold = pct">{{ pct }}%</button>
                    </div>
                  </div>
                  <button class="btn-start-annotation" style="background: var(--color-accent);" :disabled="modelAnnotationLoading || !selectedPersistentModelId" @click="runModelInference">
                    <svg v-if="modelAnnotationLoading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" class="spin"><circle cx="12" cy="12" r="10" stroke-opacity="0.2" /><path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" /></svg>
                    <span>{{ modelAnnotationLoading ? '推理中...' : '执行模型标注' }}</span>
                  </button>
                </div>
              </div>
            </aside>

            <div class="annotation-preview-area">
              <aside class="annotation-snippet-column" v-if="annotationSnippets.length && !annotationLoading">
                <div class="snippet-column-header">
                  <div class="snippet-column-header-left">
                    <span class="snippet-column-title">命中片段</span>
                    <span class="snippet-column-count">{{ annotationSnippets.length }}</span>
                  </div>
                  <div class="snippet-column-nav">
                    <button class="snippet-column-nav-btn" title="上一段" @click="goToPrevSnippet" :disabled="currentSnippetIndex <= 0">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                        <polyline points="15 18 9 12 15 6" />
                      </svg>
                    </button>
                    <span class="snippet-column-position">{{ currentSnippetIndex + 1 }}/{{ annotationSnippets.length }}</span>
                    <button class="snippet-column-nav-btn" title="下一段" @click="goToNextSnippet" :disabled="currentSnippetIndex >= annotationSnippets.length - 1">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                        <polyline points="9 18 15 12 9 6" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="snippet-column-list">
                  <button
                    v-for="(entry, idx) in annotationSnippets"
                    :key="entry.id || idx"
                    class="annotation-snippet-card"
                    :class="{ active: idx === currentSnippetIndex }"
                    :data-entity-id="entry.id"
                    @click="goToSnippet(idx)"
                  >
                    <div class="annotation-snippet-head">
                      <span class="snippet-color-bar" :style="{ background: getSnippetColor(entry) }"></span>
                      <span class="annotation-snippet-rule">{{ entry.rule_label }}</span>
                      <span class="annotation-snippet-idx">{{ idx + 1 }}</span>
                      <span v-if="entry._sources?.includes('rule')" class="snippet-source-tag source-rule" title="来自规则标注">R</span>
                      <span v-if="entry._sources?.includes('model')" class="snippet-source-tag source-model" title="来自模型标注">M</span>
                      <span v-if="entry._sources?.includes('model') && entry.confidence != null" class="snippet-conf-badge" :class="{ 'conf-high': entry.confidence >= 0.7, 'conf-mid': entry.confidence >= 0.4, 'conf-low': true }">{{ (entry.confidence * 100).toFixed(0) }}%</span>
                    </div>
                    <p class="annotation-snippet-text">{{ entry.text }}</p>
                    <p v-if="entry.context" class="annotation-snippet-context">{{ truncateContext(entry.context, 80) }}</p>
                    <div v-if="entry.tags?.length" class="annotation-snippet-tags">
                      <span v-for="tag in entry.tags" :key="tag" class="annotation-tag">{{ tag }}</span>
                    </div>
                  </button>
                </div>
              </aside>

              <div v-else class="annotation-snippet-column-empty">
                <div class="annotation-empty-state">
                  {{ annotationLoading ? '正在分析 Markdown 中的有效信息...' : selectedAnnotationRules.length ? '当前规则下暂无明显命中内容。' : '请先选择至少一个标注规则。' }}
                </div>
              </div>

              <section class="annotation-preview-panel">
                <div class="panel-header annotation-preview-header">
                  <div class="panel-header-left">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                      <line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
                    </svg>
                    <span>Markdown 标注预览</span>
                  </div>
                  <div class="panel-header-right">
                    <span class="word-count">{{ wordCount }} 字</span>
                    <span v-if="annotationCounts.entries || annotationCounts.snippets" class="panel-hint">
                      命中 {{ annotationCounts.entries || annotationCounts.snippets }} 段 &middot; 高亮 {{ annotationCounts.entities }} 实体
                    </span>
                  </div>
                </div>
                <div class="panel-body md-body annotation-preview-body" ref="mdBodyRef">
                  <div v-if="annotationScanActive" class="annotation-scan-line" :style="{ top: scanLineY + 'px' }"><span class="annotation-scan-cursor"></span></div>
                  <div v-if="mdLoadError" class="panel-error-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="12" y1="8" x2="12" y2="12" />
                      <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    <p class="panel-error-title">Markdown 加载失败</p>
                    <p class="panel-error-desc">无法获取解析结果，请检查后端服务是否正常运行。</p>
                    <button class="btn-retry" @click="retryLoadMd">重新加载</button>
                  </div>
                  <div v-else-if="mdLoading" class="panel-loading-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32" class="spin">
                      <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                      <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                    </svg>
                    <p>正在加载解析结果...</p>
                  </div>
                  <div v-else class="md-content-wrap annotation-md-content">
                    <div :key="mdViewKey" v-html="renderedMarkdown"></div>
                  </div>
                </div>
              </section>
            </div>
          </div>

          <div class="step-bottom-nav step-bottom-nav--annotation">
            <button class="btn-secondary" @click="navigateToStep(4)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                <polyline points="15 18 9 12 15 6" />
              </svg>
              上一步：返回校对
            </button>
            <span class="step-nav-hint">修改 MD 后返回此步骤将重新分析</span>
          </div>
        </section>
      </main>

      <!-- Model Management Page -->
      <main class="app-main" v-else>
        <section class="step-view step-models">
          <div class="models-split-layout">
            <!-- ===== 左侧面板：已训练模型列表 ===== -->
            <div class="models-left-panel">
              <div class="models-left-header">
                <h3 class="models-left-title">已训练模型</h3>
                <span class="models-left-count" v-if="!modelsLoading">{{ savedModels.length }} 个</span>
              </div>
              <div class="models-left-body">
                <div v-if="modelsLoading" class="models-empty">加载中...</div>
                <div v-else-if="!savedModels.length" class="models-empty">暂无已训练的模型</div>
                <div v-else class="models-card-list">
                  <div v-for="model in savedModels" :key="model.model_id" class="models-card" :class="{ 'models-card-selected': selectedModelId === model.model_id }" @click="viewModelDetail(model.model_id)">
                    <div class="models-card-top">
                      <span class="model-name-cell">{{ model.model_name }}</span>
                      <span class="models-card-count">{{ model.example_count || 0 }} 示例</span>
                    </div>
                    <div class="models-card-tags">
                      <span v-for="label in (model.entity_labels || model.labels || [])" :key="label" class="model-label-badge">{{ label }}</span>
                    </div>
                    <div class="models-card-bottom">
                      <span class="model-time-cell">{{ model.created_at || '--' }}</span>
                      <div class="model-actions-cell">
                        <button class="btn-sm btn-download" @click.stop="downloadModel(model.model_id)">下载</button>
                        <button class="btn-sm btn-danger-text" @click.stop="deleteModelConfirmId = model.model_id">删除</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- ===== 右侧面板：训练新模型 ===== -->
            <div class="models-right-panel">
              <div class="models-right-header" style="gap:8px;">
                <button class="models-tab-btn" :class="{ active: modelsSubTab === 'train' }" @click="modelsSubTab = 'train'; selectedModelId = null">模型训练</button>
                <button class="models-tab-btn" :class="{ active: modelsSubTab === 'eval' }" @click="modelsSubTab = 'eval'; selectedModelId = null">模型评价</button>
              </div>
              <div class="models-right-body">

                <!-- TAB: 模型训练 -->
                <template v-if="modelsSubTab === 'train' && !selectedModelId">

                <!-- 训练表单 -->
                <div v-if="!isTraining" class="train-form-section">
                <!-- 第一行：文件上传 + 模型名称 -->
                <div class="train-top-row">
                  <label class="train-file-upload" :class="{ 'has-file': modelUploadFile }" @click="!isTraining && modelFileInput?.click()">
                    <div class="train-file-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                    </div>
                    <div class="train-file-text">
                      <span v-if="!modelUploadFile" class="train-file-placeholder">点击上传 JSONL 训练数据文件</span>
                      <span v-else class="train-file-name">{{ modelUploadFile.name }}</span>
                    </div>
                    <button v-if="modelUploadFile && !isTraining" class="train-file-remove" @click.stop="modelUploadFile = null" title="移除文件">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                        <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                      </svg>
                    </button>
                  </label>
                  <input ref="modelFileInput" type="file" class="hidden-input" accept=".jsonl,.json" @change="onModelFileChange" />
                  <div class="train-name-input">
                    <label class="config-label">模型名称</label>
                    <input v-model="trainModelName" class="select-field" placeholder="输入模型名称" :disabled="isTraining" />
                  </div>
                </div>

                <!-- 第二行：超参数网格 -->
                <div class="train-params-grid">
                  <div class="train-param-item">
                    <label class="config-label">Epochs</label>
                    <input v-model.number="trainEpochs" class="select-field" type="number" min="1" max="50" :disabled="isTraining" />
                  </div>
                  <div class="train-param-item">
                    <label class="config-label">Batch Size</label>
                    <input v-model.number="trainBatchSize" class="select-field" type="number" min="2" max="64" :disabled="isTraining" />
                  </div>
                  <div class="train-param-item">
                    <label class="config-label">Learning Rate</label>
                    <input v-model.number="trainLearningRate" class="select-field" type="number" step="0.00001" min="1e-6" max="0.1" :disabled="isTraining" />
                  </div>
                </div>

                <!-- 开始训练按钮 -->
                <div class="train-actions">
                  <button
                    class="btn-train-start"
                    :disabled="isTraining || !modelUploadFile || !trainModelName.trim()"
                    @click="uploadAndTrainModel"
                  >
                    <svg v-if="isTraining" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="spin">
                      <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                      <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                      <polygon points="5 3 19 12 5 21 5 3" />
                    </svg>
                    {{ isTraining ? '训练中...' : '开始训练' }}
                  </button>
                </div>

                </div>

                <!-- 可视化区域（始终占位，预训练时灰色占位，训练中显示真实图表） -->
                <div class="train-progress-area">
                  <template v-if="isTraining">
                    <!-- 训练中：真实进度和图表 -->
                    <div class="train-progress-header">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20" class="spin">
                        <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
                        <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                      </svg>
                      <span class="train-progress-title">正在训练模型...</span>
                    </div>
                    <p class="train-status-msg">{{ trainStatusMsg }}</p>
                    <div v-if="trainProgress?.val_loss != null" class="train-val-bar">
                      <span class="train-val-label">验证集</span>
                      <span class="train-val-metric">Loss {{ Number(trainProgress.val_loss).toFixed(4) }}</span>
                      <span class="train-val-sep">|</span>
                      <span class="train-val-metric">Acc {{ (Number(trainProgress.val_accuracy) * 100).toFixed(1) }}%</span>
                    </div>
                    <div class="train-progress-bar-wrap">
                      <div class="train-progress-bar">
                        <div class="train-progress-bar-fill" :style="{ width: trainProgressPercent + '%' }"></div>
                      </div>
                      <span class="train-progress-pct">{{ trainProgressPercent }}%</span>
                    </div>
                  </template>
                  <template v-else>
                    <!-- 预训练：灰色占位 -->
                    <div class="train-progress-header" style="opacity:0.4;">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                        <polygon points="5 3 19 12 5 21 5 3" />
                      </svg>
                      <span class="train-progress-title">等待开始训练...</span>
                    </div>
                    <div class="train-progress-bar-wrap" style="opacity:0.3;">
                      <div class="train-progress-bar" style="background:var(--color-border);">
                        <div class="train-progress-bar-fill" style="width:0%;"></div>
                      </div>
                      <span class="train-progress-pct">0%</span>
                    </div>
                  </template>

                  <div class="train-progress-detail">

                    <!-- ===== 训练可视化区域 ===== -->
                    <div class="train-charts-grid">
                      <!-- Loss 主图 + LR 叠加 -->
                      <div class="train-chart-card train-chart-large">
                        <div class="train-chart-card-header">
                          <span class="train-chart-card-title">Loss 曲线</span>
                          <div style="display:flex;gap:16px;align-items:center;">
                            <span class="train-chart-card-value" v-if="trainProgress?.loss_smooth != null">EMA {{ Number(trainProgress.loss_smooth).toFixed(4) }}</span>
                            <span class="train-chart-card-value" style="color:#f59e0b;" v-if="trainProgress?.learning_rate != null">LR {{ Number(trainProgress.learning_rate).toExponential(2) }}</span>
                          </div>
                        </div>
                        <div class="train-chart-body">
                          <canvas ref="lossChartCanvas"></canvas>
                        </div>
                      </div>

                      <!-- 三小图并排 -->
                      <div class="train-small-charts">
                        <!-- Grad Norm -->
                        <div class="train-chart-card">
                          <div class="train-chart-card-header">
                            <span class="train-chart-card-title">Grad Norm</span>
                            <span class="train-chart-card-value train-val-red" v-if="trainProgress?.grad_norm != null">{{ Number(trainProgress.grad_norm).toFixed(3) }}</span>
                          </div>
                          <div class="train-chart-body train-chart-sm">
                            <canvas ref="gradNormChartCanvas"></canvas>
                          </div>
                          <div class="train-chart-hint">实际更新被 clip 在 1.0 以内。平滑线下降 → 收敛中；持续接近 1.0 → 震荡。</div>
                        </div>

                        <!-- Token Accuracy -->
                        <div class="train-chart-card">
                          <div class="train-chart-card-header">
                            <span class="train-chart-card-title">Accuracy</span>
                            <span class="train-chart-card-value train-val-purple" v-if="trainProgress?.accuracy != null">{{ (Number(trainProgress.accuracy) * 100).toFixed(1) }}%</span>
                          </div>
                          <div class="train-chart-body train-chart-sm">
                            <canvas ref="accuracyChartCanvas"></canvas>
                          </div>
                        </div>

                        <!-- 训练日志 -->
                        <div class="train-chart-card" style="grid-column: span 1;">
                          <div class="train-chart-card-header">
                            <span class="train-chart-card-title">训练日志</span>
                            <span class="train-chart-card-value" style="font-size:10px;color:var(--color-text-muted);">{{ trainLogMessages.length }} 条</span>
                          </div>
                          <div class="train-chart-body train-chart-sm" style="padding:0;">
                            <pre ref="trainLogPanel" class="train-log-panel">{{ trainLogMessages.join('\n') || '等待日志...' }}</pre>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                </template>

                <!-- 模型详情视图 -->
                <div v-if="selectedModelId" class="model-detail-view">
                  <div class="model-detail-topbar">
                    <button class="btn-new-model-train" @click="selectedModelId = null; modelsSubTab = 'train'">
                      ← 新建模型训练
                    </button>
                    <span class="model-detail-name">{{ selectedModelMeta?.model_name || '' }}</span>
                  </div>
                  <div v-if="modelDetailLoading" class="models-empty">加载中...</div>
                  <div v-else-if="selectedModelMeta" class="model-detail-content">
                    <div class="model-detail-stats">
                      <span>{{ selectedModelMeta.example_count || 0 }} 训练样本</span>
                      <span>{{ selectedModelMeta.train_duration_seconds || 0 }}s 训练耗时</span>
                      <span>{{ (selectedModelMeta.entity_labels || []).length }} 标签</span>
                    </div>
                    <div class="model-detail-charts" v-if="selectedModelMeta.training_history && selectedModelMeta.training_history.length > 0">
                      <div class="train-chart-card train-chart-large" style="margin-bottom:12px;">
                        <div class="train-chart-card-header">
                          <span class="train-chart-card-title">Loss / LR 曲线</span>
                        </div>
                        <div class="train-chart-body" style="height:170px;position:relative;">
                          <canvas ref="historyLossChartCanvas"></canvas>
                        </div>
                      </div>
                      <div class="train-chart-card">
                        <div class="train-chart-card-header">
                          <span class="train-chart-card-title">Grad Norm</span>
                        </div>
                        <div class="train-chart-body" style="height:120px;position:relative;">
                          <canvas ref="historyGradChartCanvas"></canvas>
                        </div>
                      </div>
                    </div>
                    <div v-else class="models-empty">该模型无训练历史数据</div>
                  </div>
                </div>
                <div v-if="modelsSubTab === 'eval' && savedModels.length > 0" class="eval-section">
                  <div class="eval-section-header">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                      <path d="M9 11l3 3L22 4" />
                      <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
                    </svg>
                    <span>评估模型</span>
                  </div>

                  <div class="eval-form">
                    <select v-model="evalModelId" class="select-field" style="flex:1;">
                      <option value="">-- 选择要评估的模型 --</option>
                      <option v-for="m in savedModels" :key="m.model_id" :value="m.model_id">{{ m.model_name }} ({{ (m.entity_labels || []).length }} 标签)</option>
                    </select>

                    <label class="train-file-upload eval-file-upload" :class="{ 'has-file': evalTestFile }" @click="!isEvaluating && evalFileInput?.click()">
                      <div class="train-file-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                          <polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
                        </svg>
                      </div>
                      <div class="train-file-text">
                        <span v-if="!evalTestFile" class="train-file-placeholder">上传测试 JSONL</span>
                        <span v-else class="train-file-name">{{ evalTestFile.name }}</span>
                      </div>
                    </label>
                    <input ref="evalFileInput" type="file" class="hidden-input" accept=".jsonl,.json" @change="onEvalFileChange" />

                    <button
                      class="btn-train-start"
                      style="width:auto;padding:10px 24px;"
                      :disabled="isEvaluating || !evalTestFile || !evalModelId.trim()"
                      @click="runEvaluation"
                    >
                      <svg v-if="isEvaluating" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" class="spin">
                        <circle cx="12" cy="12" r="10" stroke-opacity="0.2" /><path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
                      </svg>
                      <span>{{ isEvaluating ? '评估中...' : '开始评估' }}</span>
                    </button>
                  </div>

                  <!-- 评估结果 -->
                  <div v-if="evalResult" class="eval-results">
                    <div class="eval-metrics-row">
                      <div class="eval-metric-card">
                        <span class="eval-metric-value">{{ (evalResult.overall.precision * 100).toFixed(1) }}%</span>
                        <span class="eval-metric-label">Precision</span>
                      </div>
                      <div class="eval-metric-card">
                        <span class="eval-metric-value">{{ (evalResult.overall.recall * 100).toFixed(1) }}%</span>
                        <span class="eval-metric-label">Recall</span>
                      </div>
                      <div class="eval-metric-card">
                        <span class="eval-metric-value">{{ (evalResult.overall.f1 * 100).toFixed(1) }}%</span>
                        <span class="eval-metric-label">F1 Score</span>
                      </div>
                      <div class="eval-metric-card">
                        <span class="eval-metric-value">{{ evalResult.sample_count }}</span>
                        <span class="eval-metric-label">测试样本</span>
                      </div>
                    </div>

                    <!-- 每类 F1 柱状图 -->
                    <div v-if="evalResult.per_class && Object.keys(evalResult.per_class).length > 0" class="eval-chart-container">
                      <div class="train-chart-card-header" style="padding:8px 0;">
                        <span class="train-chart-card-title">每类 F1 得分</span>
                      </div>
                      <div style="height:160px;position:relative;">
                        <canvas ref="evalF1ChartCanvas"></canvas>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </section>
      </main>

      <!-- 模型删除确认对话框 -->
      <transition name="fade">
        <div v-if="deleteModelConfirmId" class="confirm-overlay" @click.self="deleteModelConfirmId = null">
          <div class="confirm-dialog">
            <div class="confirm-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24" height="24">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
            </div>
            <p class="confirm-title">确认删除模型</p>
            <p class="confirm-desc">此操作将永久删除该模型及其相关文件，不可恢复。确定要继续吗？</p>
            <div class="confirm-actions">
              <button class="btn-confirm-cancel" @click="deleteModelConfirmId = null">取消</button>
              <button class="btn-confirm-delete" @click="confirmDeleteModel">确认删除</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- 训练完成弹窗 -->
      <transition name="fade">
        <div v-if="showTrainCompleteModal" class="confirm-overlay" @click.self="closeTrainCompleteModal">
          <div class="confirm-dialog" style="text-align:left;max-width:420px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
              <div class="confirm-icon" style="background:var(--color-success-light);color:var(--color-success);margin:0;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24" height="24">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              </div>
              <p class="confirm-title" style="margin:0;">训练完成</p>
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:20px;padding:12px;background:var(--color-bg-subtle);border-radius:8px;">
              <div style="display:flex;justify-content:space-between;"><span style="color:var(--color-text-secondary);">模型名称</span><span style="font-weight:600;">{{ trainCompleteResult?.model_name || '--' }}</span></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:var(--color-text-secondary);">训练耗时</span><span style="font-weight:600;">{{ trainCompleteResult?.train_duration_seconds || 0 }}s</span></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:var(--color-text-secondary);">最终 Loss</span><span style="font-weight:600;color:#10b981;">{{ trainProgress?.finalLoss != null ? Number(trainProgress.finalLoss).toFixed(4) : '--' }}</span></div>
            </div>
            <div class="confirm-actions">
              <button class="btn-confirm-delete" style="background:var(--color-primary);" @click="closeTrainCompleteModal">关闭</button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <transition-group name="toast" tag="div" class="toast-container">
      <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
        <div class="toast-icon">
          <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          <svg v-else-if="toast.type === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <circle cx="12" cy="12" r="10" /><line x1="12" y1="16" x2="12" y2="12" /><line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
        </div>
        <span class="toast-msg">{{ toast.message }}</span>
      </div>
    </transition-group>

    <transition name="fade">
      <div v-if="pendingDeleteId" class="confirm-overlay" @click.self="cancelDelete">
        <div class="confirm-dialog">
          <div class="confirm-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24" height="24">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
          </div>
          <p class="confirm-title">确认删除</p>
          <p class="confirm-desc">此操作将永久删除该历史记录及相关文件，不可恢复。</p>
          <div class="confirm-actions">
            <button class="btn-confirm-cancel" @click="cancelDelete">取消</button>
            <button class="btn-confirm-delete" @click="confirmDeleteHistory">确认删除</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import TurndownService from 'turndown'
import { gfm } from 'turndown-plugin-gfm'
import { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, BarController, BarElement, Title, Tooltip, Legend, Filler } from 'chart.js'
Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, BarController, BarElement, Title, Tooltip, Legend, Filler)
// quickTrainShortcuts 已移除 —— 训练功能已迁移至模型管理页面

function resolveApiBase() {
  return ''
}
const API_BASE = resolveApiBase()
const FALLBACK_ANNOTATION_RULES = [
  { id: 'standards', label: '标准条文', description: '识别 GB、GB/T、ISO、IEC、SJ/T 等标准编号，并提取所在句子。' },
  { id: 'decisions', label: '判定结论', description: '提取包含判定结果、符合性、阴性/阳性、合格/不合格等关键信息的句子。' },
  { id: 'dates', label: '日期节点', description: '提取发布日期、实施日期及其他明显的日期信息。' },
  { id: 'limits', label: '限值指标', description: '提取 ppm、mg/kg、百分比等明显指标及对应语句。' },
  { id: 'numeric_facts', label: '数值信息', description: '提取 CAS 号、比例、网格尺寸、电压尺寸和其他与数值相关的关键信息。' }
]

const turndownService = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced',
  emDelimiter: '*',
  bulletListMarker: '-',
})

turndownService.use(gfm)

const fileInput = ref(null)
const mdBodyRef = ref(null)
const editableRef = ref(null)
const mdViewKey = ref(0)
const selectedFile = ref(null)
const isDragOver = ref(false)
const pdfUrl = ref('')
const renderedMarkdown = ref('')
const rawMarkdown = ref('')
const splitMode = ref('horizontal')
const pdfFullscreen = ref(false)
const mdFullscreen = ref(false)
const sidebarCollapsed = ref(false)
const isDarkMode = ref(false)
const wizardStep = ref(1)
const currentPage = ref('console') // 'console' | 'models'
const annotationMode = ref('rules') // 'rules' | 'model'
const selectedPersistentModelId = ref('')
const modelAnnotationLoading = ref(false)
const savedModels = ref([])
const modelsLoading = ref(false)
const modelsSubTab = ref('train')
const selectedModelId = ref(null)
const selectedModelMeta = ref(null)
const modelDetailLoading = ref(false)
// 模型管理页面状态
const modelFileInput = ref(null)
const modelUploadFile = ref(null)
const trainModelName = ref('')
const trainEpochs = ref(2)
const trainBatchSize = ref(8)
const trainLearningRate = ref(3e-5)
const trainProgress = ref(null)
const trainStatusMsg = ref('')
const isTraining = ref(false)
const showTrainCompleteModal = ref(false)
const trainCompleteResult = ref(null)
const deleteModelConfirmId = ref(null)

// 训练历史数据（一大三小图表）
const trainLossHistory = ref([])       // {step, loss}
const trainLrHistory = ref([])         // {step, lr}
const trainGradNormHistory = ref([])   // {step, grad_norm}
const trainStartTime = ref(null)       // 训练开始时间戳
const lossChartCanvas = ref(null)
const gradNormChartCanvas = ref(null)
const accuracyChartCanvas = ref(null)
let lossChart = null
let gradNormChart = null
let accuracyChart = null
const historyLossChartCanvas = ref(null)
const historyGradChartCanvas = ref(null)
let historyLossChart = null
let historyGradChart = null
const trainLogMessages = ref([])
const trainLogPanel = ref(null)
const evalFileInput = ref(null)
const evalTestFile = ref(null)
const isEvaluating = ref(false)
const evalResult = ref(null)
const evalModelId = ref('')
const evalF1ChartCanvas = ref(null)
let evalF1Chart = null

// 训练已用时间
const trainElapsedTime = computed(() => {
  if (!trainStartTime.value) return '--'
  const diff = Math.floor((Date.now() - trainStartTime.value) / 1000)
  const m = Math.floor(diff / 60)
  const s = diff % 60
  return `${m}:${String(s).padStart(2, '0')}`
})

// Perplexity 实时计算
const trainPerplexity = computed(() => {
  if (trainProgress.value?.loss == null) return null
  return Math.exp(Number(trainProgress.value.loss))
})

// Epoch 环形进度百分比
const epochRingPercent = computed(() => {
  if (!trainProgress.value || !trainProgress.value.epoch) return 0
  return Math.round((trainProgress.value.epoch / trainEpochs.value) * 100)
})

// Epoch 环形进度 conic-gradient
const epochRingGradient = computed(() => {
  const pct = epochRingPercent.value
  return `conic-gradient(#6366f1 ${pct * 3.6}deg, rgba(99,102,241,0.12) ${pct * 3.6}deg)`
})
const isUploading = ref(false)
const loadingOptions = ref(true)
const pdfLoading = ref(false)
const pdfLoadError = ref(false)
const mdLoading = ref(false)
const mdLoadError = ref(false)
const isEditing = ref(false)
const isSaving = ref(false)
const nowTick = ref(Date.now())
const annotationRules = ref(FALLBACK_ANNOTATION_RULES)
const selectedAnnotationRules = ref([])
const annotationLoading = ref(false)
const annotationError = ref('')
const annotationResult = ref({ rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } })
const modelAnnotationResult = ref({ rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } })
// highlightHtmlContent 单次 DOM 遍历后返回的实体消费顺序，用于构建命中片段
const _consumedEntities = ref([])
const modelConfThreshold = ref(0)
const annotationLastRunAt = ref(0)
const modelAnnotationLastRunAt = ref(0)
const currentSnippetIndex = ref(0)
const annotationScanActive = ref(false)
const scanLineY = ref(0)
const annotationSettingsExpanded = ref(true)

const historyRecords = ref([])
const isHistoryLoading = ref(false)
const pendingDeleteId = ref(null)

const toasts = reactive([])
let toastId = 0

// ── 动态标签颜色系统 ──
const LABEL_COLOR_PALETTE = [
  [59, 130, 246],   // 蓝
  [16, 185, 129],   // 绿
  [245, 158, 11],   // 橙
  [139, 92, 246],   // 紫
  [236, 72, 153],   // 粉
  [99, 102, 241],   // 靛
  [20, 184, 166],   // 青
  [249, 115, 22],   // 橘
  [14, 165, 233],   // 天蓝
  [168, 85, 247],   // 紫罗兰
  [34, 197, 94],    // 翠绿
  [225, 29, 72],    // 玫红
  [250, 204, 21],   // 黄
  [107, 114, 128],  // 灰
  [59, 130, 246],   // 蓝(循环)
]
const _labelColorCache = new Map()
let _labelColorNext = 0

function getLabelColor(label) {
  if (!label) return LABEL_COLOR_PALETTE[13]  // 灰 fallback
  if (_labelColorCache.has(label)) return _labelColorCache.get(label)
  const [r, g, b] = LABEL_COLOR_PALETTE[_labelColorNext % LABEL_COLOR_PALETTE.length]
  _labelColorNext++
  const color = { bg: `rgba(${r},${g},${b},0.28)`, border: `rgba(${r},${g},${b},0.6)`, solid: `rgba(${r},${g},${b},0.7)` }
  _labelColorCache.set(label, color)
  return color
}

function ensureLabelStyles() {
  // 动态注入 CSS 规则（用原始 label 做类名，中文在 CSS3 中合法）
  const styleId = '_annotation_label_styles'
  let el = document.getElementById(styleId)
  if (!el) {
    el = document.createElement('style')
    el.id = styleId
    document.head.appendChild(el)
  }
  let css = ''
  for (const [label, color] of _labelColorCache) {
    css += `.annotation-highlight.annotation-${label}{background:${color.bg};border-bottom-color:${color.border};color:inherit;}\n`
  }
  el.textContent = css
}
function showToast(message, type = 'info') {
  const id = ++toastId
  toasts.push({ id, message, type })
  setTimeout(() => {
    const idx = toasts.findIndex(t => t.id === id)
    if (idx !== -1) toasts.splice(idx, 1)
  }, 3500)
}

const availableOptions = reactive({
  backend_types: [],
  languages: [],
  ocr_modes: [],
  feature_toggles: [],
  defaults: {}
})

const parseConfig = reactive({
  backend_type: 'pipeline',
  language: 'auto',
  ocr_mode: 'auto',
  high_accuracy: true,
  enable_ocr: true,
  enable_layout: true,
  enable_formula: false,
  enable_table: true,
  enable_image: true,
  enable_heading: true,
  preserve_whitespace: true
})

const taskInfo = reactive({
  task_id: null,
  status: 'idle',
  progress: 0,
  message: '',
  file_name: '',
  feature_summary: []
})

let pollingInterval = null
let clockTimer = null

const wizardSteps = [
  { key: 'upload', label: '上传文件' },
  { key: 'config', label: '配置参数' },
  { key: 'processing', label: '解析中' },
  { key: 'review', label: '结果校对' },
  { key: 'annotation', label: '快速标注' }
]

const stages = [
  { label: '初始化', threshold: 8 },
  { label: '语言策略', threshold: 18 },
  { label: '版面分析', threshold: 32 },
  { label: 'OCR 识别', threshold: 52 },
  { label: '内容提取', threshold: 76 },
  { label: '生成结果', threshold: 100 }
]

const currentStage = computed(() => {
  if (typeof taskInfo.stage_index === 'number' && taskInfo.stage_index >= 0) {
    return Math.min(taskInfo.stage_index, stages.length - 1)
  }
  for (let i = stages.length - 1; i >= 0; i--) {
    if (taskInfo.progress >= stages[i].threshold) return i
  }
  return 0
})

const statusText = computed(() => {
  switch (taskInfo.status) {
    case 'processing': return '处理中'
    case 'completed': return '已完成'
    case 'failed': return '失败'
    default: return '就绪'
  }
})

const currentPageTitle = computed(() => {
  if (currentPage.value === 'models') return '模型管理'
  const titles = ['上传文件', '配置参数', '解析中', '结果校对', '快速标注']
  return titles[wizardStep.value - 1] || '新建任务'
})

const configPreviewTags = computed(() => {
  const tags = [
    getLabel(availableOptions.backend_types, parseConfig.backend_type),
    getLabel(availableOptions.languages, parseConfig.language),
    getLabel(availableOptions.ocr_modes, parseConfig.ocr_mode)
  ]
  availableOptions.feature_toggles.forEach(item => {
    if (parseConfig[item.key]) tags.push(item.label)
  })
  return tags
})

const wordCount = computed(() => {
  if (!rawMarkdown.value) return 0
  return rawMarkdown.value.replace(/\s+/g, '').length
})

/**
 * 收集所有标注结果中的实体（规则 + 模型），只做收集和置信度过滤，不做排序。
 * 排序和命中片段的构建由 highlightHtmlContent 单次 DOM 遍历统一完成。
 */
function mergeAnnotationResults() {
  const rule = annotationResult.value || { rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } }
  const model = modelAnnotationResult.value || { rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } }

  // Merge rules: deduplicate by id, sum counts
  const ruleMap = new Map()
  const addRule = (r, source) => {
    const existing = ruleMap.get(r.id)
    if (existing) {
      existing.count = (existing.count || 0) + (r.count || 0)
    } else {
      ruleMap.set(r.id, { ...r, _source: source })
    }
  }
  (rule.rules || []).forEach(r => addRule(r, 'rule'))
  ;(model.rules || []).forEach(r => addRule(r, 'model'))

  // 收集所有实体：规则实体全收，模型实体按置信度过滤
  const confThreshold = modelConfThreshold.value / 100
  const allEntities = []
  const addEntity = (e, source) => {
    allEntities.push({ ...e, _sources: [source] })
  }
  ;(rule.entities || []).forEach(e => addEntity(e, 'rule'))
  ;(model.entities || [])
    .filter(e => (e.confidence ?? 1) >= confThreshold)
    .forEach(e => addEntity(e, 'model'))

  const mergedRules = [...ruleMap.values()]
  const mergedSnippets = [...(rule.snippets || []), ...(model.snippets || [])]

  return {
    rules: mergedRules,
    entities: allEntities,  // 未排序，由 highlightHtmlContent 实际 DOM 遍历决定顺序
    snippets: mergedSnippets,
    counts: {
      entities: allEntities.length,
      snippets: mergedSnippets.length,
      rules: mergedRules.length,
    },
  }
}

const mergedResult = computed(() => mergeAnnotationResults())

// 命中片段：直接使用 highlightHtmlContent 一次 DOM 遍历返回的消费顺序
// 与 Markdown 中的高亮标记 1:1 精确对应
const annotationSnippets = computed(() => {
  const consumed = _consumedEntities.value
  if (consumed.length === 0) {
    // 尚未运行高亮时回退到 snippets
    return mergedResult.value?.snippets || []
  }
  return consumed.map((ent, idx) => ({
    id: ent.id,
    rule_id: ent.rule_id,
    rule_label: ent.rule_label,
    text: ent.text,
    context: ent.context || '',
    tags: [ent.text],
    confidence: ent.confidence ?? null,
    _sources: ent._sources || [],
  }))
})

const annotationCounts = computed(() => {
  const consumed = _consumedEntities.value
  const m = mergedResult.value
  return {
    entities: consumed.length || (m?.entities?.length || 0),
    entries: consumed.length,
    snippets: m?.snippets?.length || 0,
    rules: m?.rules?.length || 0,
  }
})

// 监听 mergedResult 变化，自动注入标签颜色样式，并刷新 Markdown 高亮
watch(mergedResult, () => {
  if (mergedResult.value?.entities) {
    for (const e of mergedResult.value.entities) {
      getLabelColor(e.rule_label || e.rule_id || e.type || 'entity')
    }
    ensureLabelStyles()
  }
  // 置信度阈值变化时 mergedResult 会重新计算（entities 过滤变化），
  // 需要同步更新 Markdown 渲染中的高亮标注
  refreshMarkdownView()
}, { deep: false })
const currentSnippet = computed(() => {
  const snippets = annotationSnippets.value
  if (!snippets.length) return null
  const idx = Math.min(Math.max(currentSnippetIndex.value, 0), snippets.length - 1)
  return snippets[idx] || null
})
const annotationUpdatedText = computed(() => {
  const parts = []
  if (annotationLastRunAt.value) parts.push(`规则：${new Date(annotationLastRunAt.value).toLocaleString('zh-CN', { hour12: false })}`)
  if (modelAnnotationLastRunAt.value) parts.push(`模型：${new Date(modelAnnotationLastRunAt.value).toLocaleString('zh-CN', { hour12: false })}`)
  if (!parts.length) return '尚未执行标注'
  return `最近标注 | ${parts.join(' · ')}`
})

const elapsed = computed(() => {
  if (!taskInfo.started_at) return 0
  return Math.max(0, Math.floor(nowTick.value / 1000 - taskInfo.started_at))
})

const estimatedRemaining = computed(() => {
  if (taskInfo.status === 'completed') return '0s'
  if (Number.isFinite(taskInfo.eta_seconds) && taskInfo.eta_seconds >= 0) {
    return formatDuration(taskInfo.eta_seconds)
  }
  if (elapsed.value < 2 || taskInfo.progress <= 0) return '--'
  const rate = taskInfo.progress / elapsed.value
  const remaining = Math.ceil((100 - taskInfo.progress) / rate)
  return remaining > 0 ? formatDuration(remaining) : '--'
})

function getLabel(items, value) {
  return items.find(item => item.value === value)?.label || value
}

function canNavigateToStep(step) {
  if (taskInfo.status === 'processing') return false
  if (step === 1) return wizardStep.value > 1
  if (step === 2) return wizardStep.value > 2
  if (step === 3) return wizardStep.value > 3
  if (step === 4) return wizardStep.value > 4
  if (step === 5) return taskInfo.status === 'completed' && (wizardStep.value === 4 || wizardStep.value === 5)
  return false
}

function navigateToStep(step) {
  if (step === 1) {
    reset()
    return
  }
  if (step === 5) {
    wizardStep.value = 5
    return
  }
  if (step === 4 && wizardStep.value === 5) {
    resetAnnotationState()
    refreshMarkdownView()
  }
  wizardStep.value = step
}

const MAX_FILE_SIZE = 50 * 1024 * 1024
const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg']

async function loadOptions() {
  try {
    loadingOptions.value = true
    const response = await axios.get(`${API_BASE}/options`)
    Object.assign(availableOptions, response.data)
    Object.assign(parseConfig, response.data.defaults || {})
  } catch {
    showToast('无法加载后端配置选项，部分功能可能不可用', 'error')
  } finally {
    loadingOptions.value = false
  }
}

function validateFile(file) {
  if (!file) return false
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    showToast(`不支持的文件格式: ${ext}，请选择 PDF、PNG 或 JPG`, 'error')
    return false
  }
  if (file.size > MAX_FILE_SIZE) {
    showToast(`文件过大 (${formatSize(file.size)})，最大支持 50MB`, 'error')
    return false
  }
  return true
}

function openFilePicker() {
  fileInput.value?.click()
}

function handleFileChange(event) {
  const file = event.target.files?.[0]
  if (file && validateFile(file)) selectedFile.value = file
  else clearFile()
}

function onDrop(event) {
  isDragOver.value = false
  const file = event.dataTransfer.files?.[0]
  if (file && validateFile(file)) selectedFile.value = file
  else clearFile()
}

function clearFile() {
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function formatDuration(totalSeconds) {
  if (!Number.isFinite(totalSeconds) || totalSeconds < 0) return '--'
  const seconds = Math.max(0, Math.floor(totalSeconds))
  if (seconds < 60) return `${seconds}s`
  const minutes = Math.floor(seconds / 60)
  const remainSeconds = seconds % 60
  if (minutes < 60) return `${minutes}m ${remainSeconds}s`
  const hours = Math.floor(minutes / 60)
  const remainMinutes = minutes % 60
  return `${hours}h ${remainMinutes}m`
}

function formatDate(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  const pad = (n) => n.toString().padStart(2, '0')
  return `${date.getMonth() + 1}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function rewriteMarkdownAssets(mdText, taskId = taskInfo.task_id) {
  if (!mdText) return ''
  if (!taskId) return mdText
  return mdText.replace(/images\//g, `${API_BASE}/result/${taskId}/images/`)
}

function resetAnnotationState() {
  annotationLoading.value = false
  annotationError.value = ''
  annotationLastRunAt.value = 0
  modelAnnotationLastRunAt.value = 0
  annotationResult.value = { rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } }
  modelAnnotationResult.value = { rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } }
  _consumedEntities.value = []
  currentSnippetIndex.value = 0
  selectedAnnotationRules.value = []
  annotationSettingsExpanded.value = true
}
function highlightHtmlContent(html, entities) {
  if (!html || !entities?.length || typeof DOMParser === 'undefined') return { html, consumedOrder: [] }

  // 确保标签颜色 CSS 已注入
  ensureLabelStyles()

  // 构建 FIFO pool：相同文本的实体按数组顺序排列
  const indexMap = new Map()
  entities.forEach((entity) => {
    if (!entity?.text) return
    const arr = indexMap.get(entity.text) || []
    arr.push(entity)
    indexMap.set(entity.text, arr)
  })
  const pools = new Map()
  for (const [txt, arr] of indexMap) {
    pools.set(txt, arr.slice())
  }

  // 收集所有唯一文本，按长度降序排列（长文本优先匹配，避免子串误匹配）
  const allTexts = new Set()
  entities.forEach(e => { if (e?.text) allTexts.add(e.text) })
  const terms = Array.from(allTexts).sort((a, b) => b.length - a.length)
  if (!terms.length) return { html, consumedOrder: [] }

  const parser = new DOMParser()
  const doc = parser.parseFromString(`<div id="annotation-root">${html}</div>`, 'text/html')
  const root = doc.getElementById('annotation-root')
  if (!root) return { html, consumedOrder: [] }

  const matcher = new RegExp(terms.map(escapeRegExp).join('|'), 'g')
  const walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT
      const parent = node.parentElement
      if (!parent) return NodeFilter.FILTER_REJECT
      if (parent.closest('.annotation-highlight')) return NodeFilter.FILTER_REJECT
      if (['SCRIPT', 'STYLE', 'CODE', 'PRE'].includes(parent.tagName)) return NodeFilter.FILTER_REJECT
      return NodeFilter.FILTER_ACCEPT
    }
  })

  const textNodes = []
  while (walker.nextNode()) textNodes.push(walker.currentNode)

  // 记录被消费的实体顺序 —— 这就是文档中实体出现的顺序
  const consumedOrder = []

  function _popEntity(matchedText) {
    const pool = pools.get(matchedText)
    if (pool && pool.length > 0) {
      const entity = pool.shift()
      consumedOrder.push(entity)
      return entity
    }
    return null
  }

  textNodes.forEach((node) => {
    const source = node.nodeValue
    if (!source) return
    matcher.lastIndex = 0
    let lastIndex = 0
    let hasMatch = false
    const fragment = doc.createDocumentFragment()
    let match
    while ((match = matcher.exec(source)) !== null) {
      hasMatch = true
      const matchedText = match[0]
      const entity = _popEntity(matchedText)
      if (match.index > lastIndex) {
        fragment.appendChild(doc.createTextNode(source.slice(lastIndex, match.index)))
      }
      const mark = doc.createElement('mark')
      if (entity) {
        const entityType = entity.rule_label || entity.rule_id || entity.type || 'entity'
        getLabelColor(entityType)
        mark.className = `annotation-highlight annotation-${entityType}`
        mark.dataset.entityId = entity.id || ''
        mark.dataset.entityType = entityType
        mark.dataset.entityText = entity.text || ''
      } else {
        // orphan 匹配不生成 mark
        fragment.appendChild(doc.createTextNode(matchedText))
        lastIndex = match.index + matchedText.length
        continue
      }
      mark.textContent = matchedText
      fragment.appendChild(mark)
      lastIndex = match.index + matchedText.length
    }
    if (!hasMatch) return
    if (lastIndex < source.length) {
      fragment.appendChild(doc.createTextNode(source.slice(lastIndex)))
    }
    node.parentNode?.replaceChild(fragment, node)
  })

  return { html: root.innerHTML, consumedOrder }
}

function buildRenderedMarkdown() {
  if (!rawMarkdown.value) { _consumedEntities.value = []; return '' }
  const html = marked.parse(rewriteMarkdownAssets(rawMarkdown.value))
  if (isEditing.value || wizardStep.value !== 5) { _consumedEntities.value = []; return html }
  const result = highlightHtmlContent(html, mergedResult.value?.entities || [])
  // 将单次 DOM 遍历得到的实体消费顺序存储，供命中片段面板使用
  _consumedEntities.value = result.consumedOrder
  return result.html
}

function refreshMarkdownView() {
  renderedMarkdown.value = buildRenderedMarkdown()
}

function getRuleCount(ruleId) {
  return mergedResult.value?.rules?.find(rule => rule.id === ruleId)?.count || 0
}

async function loadAnnotationOptions() {
  try {
    const response = await axios.get(`${API_BASE}/annotation/options`)
    annotationRules.value = response.data?.rules?.length ? response.data.rules : FALLBACK_ANNOTATION_RULES
  } catch {
    annotationRules.value = FALLBACK_ANNOTATION_RULES
  }
}

async function fetchAnnotations() {
  const tid = taskInfo.task_id
  if (!tid || !rawMarkdown.value || isEditing.value || wizardStep.value !== 5) {
    resetAnnotationState()
    refreshMarkdownView()
    return
  }

  if (!selectedAnnotationRules.value.length) {
    resetAnnotationState()
    refreshMarkdownView()
    return
  }

  annotationLoading.value = true
  annotationError.value = ''
  try {
    const response = await axios.post(`${API_BASE}/result/${tid}/annotations`, {
      rules: selectedAnnotationRules.value
    })
    annotationResult.value = response.data || { rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } }
    currentSnippetIndex.value = 0
    annotationLastRunAt.value = Date.now()
  } catch (error) {
    annotationError.value = error.response?.data?.message || '标注分析失败'
    annotationResult.value = { rules: [], entities: [], snippets: [], counts: { entities: 0, snippets: 0 } }
    currentSnippetIndex.value = 0
  } finally {
    annotationLoading.value = false
    refreshMarkdownView()
    await nextTick()
    animateAnnotationHighlights()
  }
}



function selectAllAnnotationRules() {
  selectedAnnotationRules.value = annotationRules.value.map(rule => rule.id)
}

function clearAnnotationRules() {
  selectedAnnotationRules.value = []
}

// ── Model management ──

async function fetchSavedModels() {
  modelsLoading.value = true
  try {
    const response = await axios.get(`${API_BASE}/models`)
    savedModels.value = response.data || []
  } catch {
    savedModels.value = []
  } finally {
    modelsLoading.value = false
  }
}



/**
 * 模型删除确认对话框的回调函数
 */
async function confirmDeleteModel() {
  const modelId = deleteModelConfirmId.value
  if (!modelId) return
  deleteModelConfirmId.value = null
  try {
    await axios.delete(`${API_BASE}/models/${modelId}`)
    savedModels.value = savedModels.value.filter(m => m.model_id !== modelId)
    showToast('模型已删除', 'success')
  } catch {
    showToast('删除失败', 'error')
  }
}

async function handleDeleteModel(modelId) {
  try {
    await axios.delete(`${API_BASE}/models/${modelId}`)
    savedModels.value = savedModels.value.filter(m => m.model_id !== modelId)
    showToast('模型已删除', 'success')
  } catch {
    showToast('删除失败', 'error')
  }
}

async function runModelInference() {
  if (!selectedPersistentModelId.value || !rawMarkdown.value) return
  modelAnnotationLoading.value = true
  try {
    const response = await axios.post(`${API_BASE}/model/infer`, {
      model_id: selectedPersistentModelId.value,
      document_text: rawMarkdown.value,
    })
    modelAnnotationResult.value = response.data || { entities: [], snippets: [], counts: [], rules: [] }
    modelAnnotationLastRunAt.value = Date.now()
    refreshMarkdownView()
    await nextTick()
    animateAnnotationHighlights()
    showToast('模型标注完成，结果已合并到当前视图', 'success')
  } catch (e) {
    showToast('模型推理失败: ' + (e.response?.data?.message || e.message), 'error')
  } finally {
    modelAnnotationLoading.value = false
  }
}

// ── 模型管理页面功能 ──

/**
 * 处理 JSONL 文件选择
 */
function onModelFileChange(event) {
  const file = event.target.files?.[0]
  if (file) {
    modelUploadFile.value = file
    // 自动使用文件名作为模型名称
    if (!trainModelName.value.trim()) {
      const name = file.name.replace(/\.(jsonl|json)$/i, '')
      trainModelName.value = name
    }
  }
}

/**
 * 初始化所有训练图表（Loss主图 + GradNorm + Perplexity）
 */
function initCharts() {
  const commonGrid = { color: 'rgba(148,163,184,0.08)' }
  const commonText = '#64748b'
  const commonInteraction = { intersect: false, mode: 'index' }
  const commonLegend = { labels: { color: '#94a3b8', usePointStyle: true, padding: 16, font: { size: 11 } } }

  // Destroy any existing chart instances first
  if (lossChart) { lossChart.destroy(); lossChart = null }
  if (gradNormChart) { gradNormChart.destroy(); gradNormChart = null }
  if (accuracyChart) { accuracyChart.destroy(); accuracyChart = null }

  // ── Loss 主图（双 Y 轴）──
  if (lossChartCanvas.value) {
    const lossCtx = lossChartCanvas.value.getContext('2d')
    if (lossCtx) {
      lossChart = new Chart(lossCtx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Loss (raw)',
            data: [],
            borderColor: 'rgba(148,163,184,0.35)',
            borderWidth: 0.8,
            pointRadius: 0,
            tension: 0.2,
            fill: false,
            yAxisID: 'y',
            borderDash: [3, 6],
          },
          {
            label: 'Loss (smooth)',
            data: [],
            borderColor: '#10b981',
            backgroundColor: (ctx) => {
              const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height)
              gradient.addColorStop(0, 'rgba(16,185,129,0.20)')
              gradient.addColorStop(1, 'rgba(16,185,129,0.02)')
              return gradient
            },
            borderWidth: 2.5,
            pointRadius: 0,
            tension: 0.4,
            fill: true,
            yAxisID: 'y',
          },
          {
            label: 'LR',
            data: [],
            borderColor: '#f59e0b',
            borderWidth: 1.5,
            pointRadius: 0,
            tension: 0.4,
            fill: false,
            yAxisID: 'y1',
            borderDash: [5, 3],
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 200 },
        interaction: commonInteraction,
        plugins: {
          legend: commonLegend,
          tooltip: {
            callbacks: {
              label(ctx) {
                if (ctx.datasetIndex === 0) return `Loss (raw): ${(ctx.raw || 0).toFixed(4)}`
                if (ctx.datasetIndex === 1) return `Loss (smooth): ${(ctx.raw || 0).toFixed(4)}`
                if (ctx.datasetIndex === 2) return `LR: ${(ctx.raw || 0).toExponential(2)}`
                return ''
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: { display: true, text: 'Step', color: commonText },
            ticks: { color: commonText, maxTicksLimit: 10 },
            grid: commonGrid,
          },
          y: {
            type: 'linear', display: true, position: 'left',
            title: { display: true, text: 'Loss', color: commonText },
            ticks: { color: commonText },
            grid: commonGrid,
          },
          y1: {
            type: 'linear', display: true, position: 'right',
            title: { display: true, text: 'LR', color: commonText },
            ticks: { color: commonText, callback: (v) => v.toExponential(1) },
            grid: { drawOnChartArea: false },
          }
        }
      }
    })
    }
  }

  // ── Grad Norm 小图 ──
  if (gradNormChartCanvas.value) {
    const gnCtx = gradNormChartCanvas.value.getContext('2d')
    if (gnCtx) {
    gradNormChart = new Chart(gnCtx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Grad Norm',
            data: [],
            borderColor: 'rgba(239,68,68,0.5)',
            backgroundColor: 'rgba(239,68,68,0.08)',
            borderWidth: 1.5,
            pointRadius: 1.5,
            pointBackgroundColor: 'rgba(239,68,68,0.8)',
            tension: 0.35,
            fill: false,
          },
          {
            label: 'Smooth',
            data: [],
            borderColor: '#ef4444',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.5,
            fill: false,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 200 },
        interaction: commonInteraction,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            display: true,
            ticks: { color: commonText, maxTicksLimit: 5, font: { size: 10 } },
            grid: commonGrid,
          },
          y: {
            display: true,
            title: { display: false },
            ticks: { color: commonText, font: { size: 10 } },
            grid: commonGrid,
          }
        }
      }
    })
    }
  }

  // ── Token Accuracy 小图 ──
  if (accuracyChartCanvas.value) {
    const acCtx = accuracyChartCanvas.value.getContext('2d')
    if (acCtx) {
    accuracyChart = new Chart(acCtx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Accuracy',
            data: [],
            borderColor: '#8b5cf6',
            backgroundColor: (ctx) => {
              const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height)
              gradient.addColorStop(0, 'rgba(139,92,246,0.15)')
              gradient.addColorStop(1, 'rgba(139,92,246,0.02)')
              return gradient
            },
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.4,
            fill: true,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 200 },
        interaction: commonInteraction,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label(ctx) { return `Accuracy: ${((ctx.raw || 0) * 100).toFixed(1)}%` }
            }
          }
        },
        scales: {
          x: {
            display: true,
            ticks: { color: commonText, maxTicksLimit: 5, font: { size: 10 } },
            grid: commonGrid,
          },
          y: {
            display: true,
            title: { display: false },
            min: 0,
            max: 1,
            ticks: { color: commonText, font: { size: 10 }, callback: (v) => `${(v * 100).toFixed(0)}%` },
            grid: commonGrid,
          }
        }
      }
    })
    }
  }
}

/**
 * 计算简单移动平均（用于平滑线）
 */
function smoothArray(values, windowSize = 5) {
  if (!values || values.length === 0) return []
  const result = []
  for (let i = 0; i < values.length; i++) {
    const start = Math.max(0, i - Math.floor(windowSize / 2))
    const end = Math.min(values.length, i + Math.floor(windowSize / 2) + 1)
    const slice = values.slice(start, end)
    result.push(slice.reduce((a, b) => a + b, 0) / slice.length)
  }
  return result
}

/**
 * 更新所有训练图表数据
 */
function updateCharts(step, lossSmooth, lossRaw, lr, gradNorm, accuracy) {
  // 追加历史数据（保存 EMA 平滑值作为主 loss）
  trainLossHistory.value.push({ step, loss: lossSmooth, loss_raw: lossRaw })
  trainLrHistory.value.push({ step, lr })
  trainGradNormHistory.value.push({ step, grad_norm: gradNorm })

  // 更新 Loss 主图
  if (lossChart) {
    lossChart.data.labels.push(step)
    lossChart.data.datasets[0].data.push(lossRaw != null ? lossRaw : lossSmooth)
    lossChart.data.datasets[1].data.push(lossSmooth)
    lossChart.data.datasets[2].data.push(lr)
    lossChart.update()
  }

  // 更新 Grad Norm 小图
  if (gradNormChart) {
    gradNormChart.data.labels.push(step)
    gradNormChart.data.datasets[0].data.push(gradNorm)
    const recentGrads = trainGradNormHistory.value.map(d => d.grad_norm)
    const smoothed = smoothArray(recentGrads, 5)
    gradNormChart.data.datasets[1].data = smoothed
    gradNormChart.update()
  }

  // 更新 Token Accuracy 小图
  if (accuracyChart) {
    if (accuracy != null) {
      accuracyChart.data.labels.push(step)
      accuracyChart.data.datasets[0].data.push(accuracy)
      accuracyChart.update()
    }
  }
}

/**
 * 上传 JSONL 文件并开始训练（SSE 流）
 */
async function uploadAndTrainModel() {
  if (!modelUploadFile.value || !trainModelName.value.trim() || isTraining.value) return

  isTraining.value = true
  trainProgress.value = null
  trainStatusMsg.value = '正在上传训练数据...'
  trainStartTime.value = Date.now()

  // 重置历史数据
  trainLossHistory.value = []
  trainLrHistory.value = []
  trainGradNormHistory.value = []
  trainLogMessages.value = []

  // 销毁旧图表
  if (lossChart && typeof lossChart.destroy === 'function') { lossChart.destroy(); lossChart = null }
  if (gradNormChart && typeof gradNormChart.destroy === 'function') { gradNormChart.destroy(); gradNormChart = null }
  if (accuracyChart && typeof accuracyChart.destroy === 'function') { accuracyChart.destroy(); accuracyChart = null }
  await nextTick()
  initCharts()

  const formData = new FormData()
  formData.append('file', modelUploadFile.value)
  formData.append('model_name', trainModelName.value.trim())
  formData.append('epochs', String(trainEpochs.value))
  formData.append('batch_size', String(trainBatchSize.value))
  formData.append('lr', String(trainLearningRate.value))

  try {
    const response = await fetch(`${API_BASE}/model/upload-and-train`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      let errMsg = `服务器错误 (${response.status})`
      try {
        const errData = await response.json()
        errMsg = errData.message || errMsg
      } catch (_) { /* ignore parse error */ }
      throw new Error(errMsg)
    }

    if (!response.body) {
      throw new Error('服务器返回空响应')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let trainingCompleted = false

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      const lines = buffer.split('\n')
      buffer = lines.pop()

      for (const line of lines) {
        if (trainingCompleted) continue
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.type === 'status') {
              trainStatusMsg.value = data.message
            } else if (data.type === 'progress') {
              trainProgress.value = data
              const currentEpoch = Math.floor(data.epoch) + 1
              trainStatusMsg.value = `Epoch ${currentEpoch}/${trainEpochs.value} · Step ${data.step}/${data.max_steps}`
              const step = data.step ?? trainLossHistory.value.length + 1
              if (data.loss != null) {
                const loss = data.loss_smooth ?? data.loss
                const lossRaw = data.loss
                const lr = data.learning_rate ?? 0
                const gradNorm = data.grad_norm ?? 0
                const accuracy = data.accuracy ?? null
                updateCharts(step, loss, lossRaw, lr, gradNorm, accuracy)
              }
            } else if (data.type === 'complete') {
              trainingCompleted = true
              // 保存最终 Loss 用于弹窗显示
              const finalLoss = trainProgress.value?.loss
              trainProgress.value = data.result
              trainProgress.value.finalLoss = finalLoss
              trainStatusMsg.value = '训练完成！'
              trainStartTime.value = null
              await fetchSavedModels()
              showTrainCompleteModal.value = true
              trainCompleteResult.value = data.result
            } else if (data.type === 'validation') {
              trainProgress.value = { ...trainProgress.value, val_loss: data.val_loss, val_accuracy: data.val_accuracy }
              trainLogMessages.value.push(`[验证] loss=${data.val_loss.toFixed(4)} acc=${(data.val_accuracy * 100).toFixed(1)}%`)
              nextTick(() => { if (trainLogPanel.value) trainLogPanel.value.scrollTop = trainLogPanel.value.scrollHeight })
            } else if (data.type === 'error') {
              showToast('训练失败: ' + data.message, 'error')
              console.error(data.detail)
            } else if (data.type === 'log') {
              trainLogMessages.value.push(data.message)
              nextTick(() => {
                if (trainLogPanel.value) {
                  trainLogPanel.value.scrollTop = trainLogPanel.value.scrollHeight
                }
              })
            }
          } catch (parseErr) {
            // ignore non-JSON data lines
          }
        }
      }
    }
  } catch (e) {
    showToast('训练失败: ' + (e.message || '连接中断'), 'error')
  } finally {
    isTraining.value = false
    trainStartTime.value = null
  }
}

/**
 * 计算训练进度百分比
 */
const trainProgressPercent = computed(() => {
  if (!trainProgress.value || !trainProgress.value.step || !trainProgress.value.max_steps) return 0
  return Math.round((trainProgress.value.step / trainProgress.value.max_steps) * 100)
})

/**
 * 关闭训练完成弹窗
 */
function closeTrainCompleteModal() {
  showTrainCompleteModal.value = false
  trainCompleteResult.value = null
  modelUploadFile.value = null
  trainModelName.value = ''
  trainProgress.value = null
}

/**
 * 查看模型详情（点击左侧模型卡片）
 */
async function viewModelDetail(modelId) {
  selectedModelId.value = modelId
  modelDetailLoading.value = true
  selectedModelMeta.value = null
  try {
    const response = await axios.get(`${API_BASE}/models/${modelId}`)
    selectedModelMeta.value = response.data
    modelDetailLoading.value = false
    // 用 setTimeout 确保 Vue 完成 canvas DOM 渲染后再画图
    setTimeout(() => renderHistoryCharts(), 80)
  } catch {
    modelDetailLoading.value = false
    showToast('加载模型详情失败', 'error')
  }
}

/**
 * 渲染模型历史训练曲线
 */
function renderHistoryCharts() {
  const meta = selectedModelMeta.value
  if (!meta || !meta.training_history || !meta.training_history.length) return

  if (historyLossChart) { historyLossChart.destroy(); historyLossChart = null }
  if (historyGradChart) { historyGradChart.destroy(); historyGradChart = null }

  const history = meta.training_history
  const steps = history.map(d => d.step)
  const losses = history.map(d => d.loss_smooth ?? d.loss)
  const lossesRaw = history.map(d => d.loss)
  const lrs = history.map(d => d.learning_rate)
  const gradNorms = history.map(d => d.grad_norm)

  const commonGrid = { color: 'rgba(148,163,184,0.08)' }
  const commonText = '#64748b'

  if (historyLossChartCanvas.value) {
    const ctx = historyLossChartCanvas.value.getContext('2d')
    if (ctx) {
      historyLossChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: steps,
          datasets: [
            { label: 'Loss (raw)', data: lossesRaw, borderColor: 'rgba(148,163,184,0.35)', borderWidth: 0.8, pointRadius: 0, tension: 0.2, fill: false, yAxisID: 'y', borderDash: [3,6] },
            { label: 'Loss (smooth)', data: losses, borderColor: '#10b981', borderWidth: 2, pointRadius: 0, tension: 0.4, fill: true, yAxisID: 'y',
              backgroundColor: (c) => { const g = c.chart.ctx.createLinearGradient(0,0,0,c.chart.height); g.addColorStop(0,'rgba(16,185,129,0.15)'); g.addColorStop(1,'rgba(16,185,129,0.02)'); return g; }
            },
            { label: 'LR', data: lrs, borderColor: '#f59e0b', borderWidth: 1.5, pointRadius: 0, tension: 0.4, fill: false, yAxisID: 'y1', borderDash: [5,3] }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          interaction: { intersect: false, mode: 'index' },
          plugins: {
            legend: { labels: { color: '#94a3b8', usePointStyle: true, padding: 16, font: { size: 11 } } },
            tooltip: {
              callbacks: {
                label(ctx) {
                  if (ctx.datasetIndex === 1) return `LR: ${(ctx.raw || 0).toExponential(2)}`
                  return `Loss: ${(ctx.raw || 0).toFixed(4)}`
                }
              }
            }
          },
          scales: {
            x: { ticks: { color: commonText, maxTicksLimit: 10 }, grid: commonGrid },
            y: { type: 'linear', position: 'left', title: { display: true, text: 'Loss', color: commonText }, ticks: { color: commonText }, grid: commonGrid },
            y1: { type: 'linear', position: 'right', title: { display: true, text: 'LR', color: commonText }, ticks: { color: commonText, callback: v => v.toExponential(1) }, grid: { drawOnChartArea: false } }
          }
        }
      })
    }
  }

  if (historyGradChartCanvas.value) {
    const ctx = historyGradChartCanvas.value.getContext('2d')
    if (ctx) {
      historyGradChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: steps,
          datasets: [
            { label: 'Grad Norm', data: gradNorms, borderColor: '#ef4444', borderWidth: 1.5, pointRadius: 0, tension: 0.35, fill: false }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          interaction: { intersect: false, mode: 'index' },
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: commonText, maxTicksLimit: 10, font: { size: 10 } }, grid: commonGrid },
            y: { ticks: { color: commonText, font: { size: 10 } }, grid: commonGrid }
          }
        }
      })
    }
  }
}

/**
 * 下载模型文件
 */
function downloadModel(modelId) {
  const link = document.createElement('a')
  link.href = `${API_BASE}/model/download/${modelId}`
  link.download = ''
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function onEvalFileChange(event) {
  const file = event.target.files?.[0]
  if (file) evalTestFile.value = file
}

async function runEvaluation() {
  if (!evalTestFile.value || !evalModelId.value.trim() || isEvaluating.value) return

  isEvaluating.value = true
  evalResult.value = null

  const formData = new FormData()
  formData.append('file', evalTestFile.value)
  formData.append('model_id', evalModelId.value.trim())

  try {
    const response = await axios.post(`${API_BASE}/model/evaluate`, formData)
    evalResult.value = response.data

    // 画每类 F1 柱状图
    await nextTick()
    if (evalF1ChartCanvas.value) {
      if (evalF1Chart) evalF1Chart.destroy()
      const ctx = evalF1ChartCanvas.value.getContext('2d')
      if (ctx) {
        const perClass = evalResult.value.per_class || {}
        const labels = Object.keys(perClass)
        const f1Values = labels.map(l => perClass[l].f1)
        const colors = labels.map((_, i) => {
          const hue = (i * 137.5) % 360
          return `hsla(${hue}, 65%, 55%, 0.8)`
        })
        evalF1Chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [{
              label: 'F1 Score',
              data: f1Values,
              backgroundColor: colors,
              borderRadius: 4,
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { beginAtZero: true, max: 1, ticks: { callback: v => (v * 100).toFixed(0) + '%' } }
            }
          }
        })
      }
    }
    showToast('评估完成', 'success')
  } catch (e) {
    showToast('评估失败: ' + (e.response?.data?.message || e.message), 'error')
  } finally {
    isEvaluating.value = false
  }
}

// Watch page switch to load models
watch(currentPage, (page) => {
  if (page === 'models') fetchSavedModels()
})

function focusAnnotation(entry) {
  if (!mdBodyRef.value) return

  let targetEl = null

  // 按 entity-id 精确匹配
  if (entry?.id) {
    targetEl = mdBodyRef.value.querySelector(
      `.annotation-highlight[data-entity-id="${CSS.escape(entry.id)}"]`
    )
  }

  // 回退：按 entity text 匹配（处理极端情况）
  if (!targetEl && entry?.text) {
    targetEl = mdBodyRef.value.querySelector(
      `.annotation-highlight[data-entity-text="${CSS.escape(entry.text)}"]`
    )
  }

  if (!targetEl) {
    showToast('未找到对应高亮', 'info')
    return
  }

  targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
  targetEl.classList.add('annotation-highlight-focus')
  window.setTimeout(() => {
    targetEl.classList.remove('annotation-highlight-focus')
  }, 2000)
}

function getSnippetColor(snippet) {
  const label = snippet?.rule_label || snippet?.rule_id || ''
  return getLabelColor(label).solid
}

function truncateContext(context, maxLen) {
  if (!context || context.length <= maxLen) return context
  return context.substring(0, maxLen) + '...'
}

function goToPrevSnippet() {
  if (currentSnippetIndex.value > 0) {
    currentSnippetIndex.value--
    focusCurrentSnippet()
    scrollActiveSnippetIntoView()
  }
}

function goToNextSnippet() {
  if (currentSnippetIndex.value < annotationSnippets.value.length - 1) {
    currentSnippetIndex.value++
    focusCurrentSnippet()
    scrollActiveSnippetIntoView()
  }
}

function goToSnippet(index) {
  if (index >= 0 && index < annotationSnippets.value.length) {
    currentSnippetIndex.value = index
    focusCurrentSnippet()
    scrollActiveSnippetIntoView()
  }
}

function scrollActiveSnippetIntoView() {
  nextTick(() => {
    const card = document.querySelector('.annotation-snippet-card.active')
    if (card) card.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
  })
}

function focusCurrentSnippet() {
  const snippet = currentSnippet.value
  if (snippet) focusAnnotation(snippet)
}

function animateAnnotationHighlights() {
  const container = mdBodyRef.value
  if (!container) return

  // Double rAF to ensure browser has finished layout after v-html update
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      _startAnnotationScan(container)
    })
  })
}

function _startAnnotationScan(container) {
  const highlights = Array.from(container.querySelectorAll('.annotation-highlight'))
  if (!highlights.length) return

  const containerRect = container.getBoundingClientRect()
  const sorted = highlights.map(el => ({
    el,
    top: el.getBoundingClientRect().top - containerRect.top + container.scrollTop
  })).sort((a, b) => a.top - b.top)

  sorted.forEach(({ el }) => el.classList.add('annotation-pending'))

  const totalHeight = container.scrollHeight
  const duration = Math.min(4200, Math.max(1600, totalHeight * 4.5))
  annotationScanActive.value = true

  const preGlowDistance = 80
  const startTime = performance.now()

  function frame(now) {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    const scanY = progress * totalHeight

    scanLineY.value = scanY

    // Pre-glow: highlights near the scan line get a warm glow before full reveal
    // Full reveal: highlights above the scan line are revealed
    sorted.forEach(({ el, top }) => {
      const dist = top - scanY
      if (dist <= 0) {
        // Passed by scan line — fully reveal
        if (el.classList.contains('annotation-pending')) {
          el.classList.remove('annotation-pending')
          el.classList.add('annotation-revealed')
        }
        el.classList.remove('annotation-glowing')
      } else if (dist <= preGlowDistance) {
        // Approaching — warm pre-glow
        el.classList.add('annotation-glowing')
      } else {
        el.classList.remove('annotation-glowing')
      }
    })

    if (progress < 1) {
      requestAnimationFrame(frame)
    } else {
      sorted.forEach(({ el }) => {
        el.classList.remove('annotation-pending', 'annotation-revealed', 'annotation-glowing')
      })
      annotationScanActive.value = false
    }
  }

  requestAnimationFrame(frame)
}

async function fetchHistory() {
  if (isHistoryLoading.value) return
  isHistoryLoading.value = true
  try {
    const response = await axios.get(`${API_BASE}/history`)
    historyRecords.value = response.data || []
  } catch (error) {
    showToast('无法加载历史记录', 'error')
  } finally {
    isHistoryLoading.value = false
  }
}

async function confirmDeleteHistory() {
  const taskId = pendingDeleteId.value
  if (!taskId) return
  pendingDeleteId.value = null
  try {
    await axios.delete(`${API_BASE}/history/${taskId}`)
    historyRecords.value = historyRecords.value.filter(r => r.task_id !== taskId)
    if (taskInfo.task_id === taskId) {
      Object.assign(taskInfo, {
        task_id: null,
        status: 'idle',
        progress: 0,
        message: '',
        file_name: '',
        feature_summary: []
      })
      wizardStep.value = 1
      pdfUrl.value = ''
      renderedMarkdown.value = ''
      rawMarkdown.value = ''
    }
    showToast('历史记录已删除', 'success')
  } catch (e) {
    const msg = e.response?.data?.message || e.message || '网络错误'
    showToast(`删除失败: ${msg}`, 'error')
  }
}

function cancelDelete() {
  pendingDeleteId.value = null
}

async function loadHistoryTask(record) {
  if (taskInfo.task_id === record.task_id) return
  
  reset()
  Object.assign(taskInfo, {
    task_id: record.task_id,
    file_name: record.file_name,
    status: record.status,
    progress: record.status === 'completed' ? 100 : 0,
    feature_summary: record.feature_summary || []
  })
  
  if (record.status === 'completed') {
    wizardStep.value = 4
    await fetchResults()
  } else if (record.status === 'failed') {
    wizardStep.value = 3
    taskInfo.message = '该任务已失败'
  } else {
    wizardStep.value = 3
    startPolling()
  }
  
  if (window.innerWidth <= 768) {
    sidebarCollapsed.value = true
  }
}

function startClock() {
  stopClock()
  nowTick.value = Date.now()
  clockTimer = setInterval(() => {
    nowTick.value = Date.now()
  }, 1000)
}

async function uploadFile() {
  if (!selectedFile.value || isUploading.value) return
  isUploading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  Object.entries(parseConfig).forEach(([key, value]) => formData.append(key, String(value)))
  try {
    const response = await axios.post(`${API_BASE}/upload`, formData)
    Object.assign(taskInfo, response.data)
    startClock()
    wizardStep.value = 3
    fetchHistory() // Refresh history after upload
    startPolling()
  } catch (error) {
    const message = error.response?.data?.detail || error.message || '未知错误'
    showToast(`上传失败: ${message}`, 'error')
  } finally {
    isUploading.value = false
  }
}

function stopPolling() {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

function stopClock() {
  if (clockTimer) {
    clearInterval(clockTimer)
    clockTimer = null
  }
}

function stopProcessingState() {
  stopPolling()
  stopClock()
}

function startPolling() {
  stopPolling()
  pollingInterval = setInterval(async () => {
    try {
      const response = await axios.get(`${API_BASE}/progress/${taskInfo.task_id}`)
      Object.assign(taskInfo, response.data)
      if (taskInfo.status === 'completed') {
        stopProcessingState()
        wizardStep.value = 4
        await fetchResults()
        showToast('文档解析完成！', 'success')
      } else if (taskInfo.status === 'failed') {
        stopProcessingState()
        showToast(`解析失败: ${taskInfo.message || '未知错误'}`, 'error')
      }
    } catch {
      // polling errors are non-fatal
    }
  }, 800)
}

async function fetchResults() {
  const tid = taskInfo.task_id
  if (!tid) return

  pdfUrl.value = `${API_BASE}/result/${tid}/pdf`
  pdfLoading.value = true
  pdfLoadError.value = false

  mdLoading.value = true
  mdLoadError.value = false
  renderedMarkdown.value = ''

  try {
    const mdResponse = await axios.get(`${API_BASE}/result/${tid}/md`)
    let mdText = mdResponse.data
    if (typeof mdText === 'object') {
      mdText = mdText.markdown || mdText.content || JSON.stringify(mdText, null, 2)
    }
    rawMarkdown.value = mdText
    refreshMarkdownView()
  } catch {
    mdLoadError.value = true
    showToast('Markdown 结果加载失败', 'error')
  } finally {
    mdLoading.value = false
    await nextTick()
  }
}

function onPdfLoad() {
  pdfLoading.value = false
  pdfLoadError.value = false
}

function onPdfError() {
  pdfLoading.value = false
  pdfLoadError.value = true
}

function retryLoadPdf() {
  pdfLoadError.value = false
  pdfLoading.value = true
  const tid = taskInfo.task_id
  if (tid) pdfUrl.value = `${API_BASE}/result/${tid}/pdf?t=${Date.now()}`
}

function retryLoadMd() {
  fetchResults()
}

async function copyMarkdown() {
  if (!rawMarkdown.value) return
  try {
    await navigator.clipboard.writeText(rawMarkdown.value)
    showToast('Markdown 已复制到剪贴板', 'success')
  } catch {
    showToast('复制失败，请手动复制', 'error')
  }
}

function startEdit() {
  const scrollTop = mdBodyRef.value?.scrollTop || 0
  isEditing.value = true
  refreshMarkdownView()
  nextTick(() => {
    if (mdBodyRef.value) {
      mdBodyRef.value.scrollTop = scrollTop
    }
    editableRef.value?.focus({ preventScroll: true })
  })
}

function persistScroll() {
  return mdBodyRef.value?.scrollTop || 0
}

function restoreScroll(top) {
  nextTick(() => {
    if (mdBodyRef.value) {
      mdBodyRef.value.scrollTop = top
    }
  })
}

function cancelEdit() {
  const scrollTop = persistScroll()
  isEditing.value = false
  refreshMarkdownView()
  mdViewKey.value++
  restoreScroll(scrollTop)
}

async function saveEdit() {
  const tid = taskInfo.task_id
  if (!tid || isSaving.value) return
  const el = editableRef.value
  if (!el) return
  isSaving.value = true
  const scrollTop = persistScroll()
  try {
    let html = el.innerHTML
    // Reverse image URL rewrites back to relative paths
    html = html.replace(new RegExp(API_BASE.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '/result/' + tid + '/images/', 'g'), 'images/')
    const mdText = turndownService.turndown(html)
    await axios.put(`${API_BASE}/result/${tid}/md`, { content: mdText })
    rawMarkdown.value = mdText
    isEditing.value = false
    resetAnnotationState()
    refreshMarkdownView()
    mdViewKey.value++
    restoreScroll(scrollTop)
    showToast('Markdown 已保存', 'success')
  } catch (e) {
    const msg = e.response?.data?.message || e.message || '保存失败'
    showToast(`保存失败: ${msg}`, 'error')
  } finally {
    isSaving.value = false
  }
}

function reset() {
  clearFile()
  stopProcessingState()
  Object.assign(taskInfo, {
    task_id: null,
    status: 'idle',
    progress: 0,
    message: '',
    file_name: '',
    feature_summary: [],
    started_at: null,
    updated_at: null,
    eta_seconds: null,
    estimated_total_seconds: null,
    stage_index: 0,
    stage_label: ''
  })
  pdfUrl.value = ''
  renderedMarkdown.value = ''
  rawMarkdown.value = ''
  splitMode.value = 'horizontal'
  pdfFullscreen.value = false
  mdFullscreen.value = false
  wizardStep.value = 1
  isUploading.value = false
  pdfLoading.value = false
  pdfLoadError.value = false
  mdLoading.value = false
  mdLoadError.value = false
  isEditing.value = false
  resetAnnotationState()
}

function startResize(event) {
  const container = event.target.closest('.panels-container')
  const isHorizontal = splitMode.value === 'horizontal'
  const startPos = isHorizontal ? event.clientX : event.clientY
  const panels = container.querySelectorAll('.panel')
  const startSize = isHorizontal ? panels[0].offsetWidth : panels[0].offsetHeight

  const onMove = (e) => {
    const delta = (isHorizontal ? e.clientX : e.clientY) - startPos
    const total = (isHorizontal ? container.clientWidth : container.clientHeight) - 6
    let ratio = ((startSize + delta) / total) * 100
    ratio = Math.max(20, Math.min(80, ratio))
    container.style.setProperty('--panel-a-pct', `${ratio}%`)
    container.style.setProperty('--panel-b-pct', `${100 - ratio}%`)
  }

  const onUp = () => {
    document.removeEventListener('mousemove', onMove)
    document.removeEventListener('mouseup', onUp)
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
  }

  document.body.style.cursor = isHorizontal ? 'col-resize' : 'row-resize'
  document.body.style.userSelect = 'none'
  document.addEventListener('mousemove', onMove)
  document.addEventListener('mouseup', onUp)
}

watch(splitMode, () => {
  pdfFullscreen.value = false
  mdFullscreen.value = false
})


watch(isDarkMode, (val) => {
  document.documentElement.classList.toggle('dark', val)
})

function onKeydown(e) {
  if (e.ctrlKey && e.key === 's' && isEditing.value) {
    e.preventDefault()
    saveEdit()
  }
}

onMounted(() => {
  loadOptions()
  loadAnnotationOptions()
  fetchHistory()
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) isDarkMode.value = true
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  stopProcessingState()
  window.removeEventListener('keydown', onKeydown)
})

</script>

<style>
/* ===== CSS Variables / Design Tokens ===== */
:root {
  --color-bg: #f0f4f8;
  --color-bg-alt: #e4eaf1;
  --color-surface: #ffffff;
  --color-surface-hover: #f8fafc;
  --color-surface-elevated: #ffffff;
  --color-primary: #5b6abf;
  --color-primary-hover: #4a56a3;
  --color-primary-light: #eef1ff;
  --color-primary-soft: #dde3ff;
  --color-accent: #d4912a;
  --color-accent-hover: #b87a22;
  --color-accent-light: #fef7ed;
  --color-success: #10b981;
  --color-success-light: #d1fae5;
  --color-warning: #f59e0b;
  --color-warning-light: #fef3c7;
  --color-danger: #ef4444;
  --color-danger-light: #fee2e2;
  --color-text: #1a2332;
  --color-text-secondary: #56657b;
  --color-text-muted: #8a99ae;
  --color-border: #dde3ed;
  --color-border-light: #eef2f7;
  --color-code-bg: #f1f5f9;
  --color-bg-subtle: #f8fafc;
  --color-overlay: rgba(15, 23, 42, 0.45);

  --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.06), 0 1px 3px rgba(15, 23, 42, 0.04);
  --shadow-lg: 0 12px 32px rgba(15, 23, 42, 0.07), 0 2px 8px rgba(15, 23, 42, 0.04);
  --shadow-xl: 0 20px 48px rgba(15, 23, 42, 0.1), 0 4px 12px rgba(15, 23, 42, 0.05);
  --shadow-card: 0 1px 2px rgba(15, 23, 42, 0.04), 0 4px 16px rgba(15, 23, 42, 0.04);

  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  --sidebar-width: 240px;
  --sidebar-collapsed-width: 64px;
  --header-height: 56px;
  --wizard-height: 52px;

  --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 0.4s cubic-bezier(0.4, 0, 0.2, 1);

  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Fira Code", "Consolas", "Monaco", monospace;
}

/* ===== Dark Theme ===== */
.app-shell.theme-dark {
  --color-bg: #0b1121;
  --color-bg-alt: #131b2f;
  --color-surface: #16213a;
  --color-surface-hover: #1c2a47;
  --color-surface-elevated: #1a2642;
  --color-primary: #8895e7;
  --color-primary-hover: #9faaef;
  --color-primary-light: #1a2045;
  --color-primary-soft: #242d5c;
  --color-accent: #e8a740;
  --color-accent-hover: #f0bc60;
  --color-accent-light: #2d2210;
  --color-success: #34d399;
  --color-success-light: #064e3b;
  --color-warning: #fbbf24;
  --color-warning-light: #78350f;
  --color-danger: #f87171;
  --color-danger-light: #7f1d1d;
  --color-text: #e8edf5;
  --color-text-secondary: #98a6c2;
  --color-text-muted: #5e6d8c;
  --color-border: #223152;
  --color-border-light: #192542;
  --color-code-bg: #1a2642;
  --color-bg-subtle: #0f1928;
  --color-overlay: rgba(0, 0, 0, 0.6);

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.35);
  --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 48px rgba(0, 0, 0, 0.45);
  --shadow-card: 0 1px 2px rgba(0, 0, 0, 0.2), 0 4px 16px rgba(0, 0, 0, 0.3);
}

/* ===== Global Reset ===== */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
  min-height: 100vh;
  overflow: hidden;
}

/* ===== App Shell Layout ===== */
.app-shell {
  display: flex;
  height: 100vh;
  background: var(--color-bg);
  transition: background var(--transition-slow);
}

/* ===== Sidebar ===== */
.app-sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100vh;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  transition: width var(--transition-base), min-width var(--transition-base);
  position: relative;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.app-sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
  min-width: var(--sidebar-collapsed-width);
  padding: 16px 8px;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 8px 12px;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
  user-select: none;
}

.sidebar-brand:hover {
  background: var(--color-surface-hover);
}

.brand-icon {
  width: 36px;
  height: 36px;
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

.app-sidebar.collapsed .brand-icon {
  background: transparent;
}

.brand-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.3px;
  white-space: nowrap;
  transition: opacity var(--transition-fast), width var(--transition-base);
}

.app-sidebar.collapsed .brand-text {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.sidebar-spacer {
  flex: 1;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 8px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 13px;
  font-family: var(--font-sans);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.nav-item svg {
  width: 18px;
  height: 18px;
  min-width: 18px;
}

.nav-item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.app-sidebar.collapsed .nav-label {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.app-sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 10px 0;
}

.sidebar-version {
  text-align: center;
  font-size: 11px;
  color: var(--color-text-muted);
  padding: 8px 0 4px;
  font-family: var(--font-mono);
  transition: opacity var(--transition-fast);
}

.app-sidebar.collapsed .sidebar-version {
  opacity: 0;
}

/* ===== History Sidebar ===== */
.sidebar-history-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  margin-top: 16px;
  overflow: hidden;
  transition: opacity var(--transition-base);
}

.sidebar-history-container.hidden {
  opacity: 0;
  pointer-events: none;
}

.sidebar-history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 8px 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-refresh-history {
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: var(--radius-xs);
  transition: all var(--transition-fast);
}

.btn-refresh-history:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.btn-new-task-sidebar {
  width: calc(100% - 8px);
  margin: 0 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 8px 0;
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-new-task-sidebar:hover {
  border-color: var(--color-primary);
  border-style: solid;
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.sidebar-history-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 4px;
}

.sidebar-history-list::-webkit-scrollbar {
  width: 4px;
}

.sidebar-history-list::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.history-empty {
  padding: 20px 8px;
  text-align: center;
  font-size: 13px;
  color: var(--color-text-muted);
}

.history-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 8px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: 4px;
}

.history-item:hover {
  background: var(--color-surface-hover);
}

.history-item.active {
  background: var(--color-primary-light);
}

.history-item-icon {
  margin-top: 2px;
  color: var(--color-text-secondary);
}

.history-item.active .history-item-icon {
  color: var(--color-primary);
}

.history-item-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-item-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-item.active .history-item-title {
  color: var(--color-primary);
  font-weight: 600;
}

.history-item-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
}

.history-item-time {
  color: var(--color-text-muted);
}

.history-item-status {
  padding: 2px 6px;
  border-radius: var(--radius-full);
  font-size: 10px;
  font-weight: 600;
}

.history-item-status.completed {
  background: var(--color-success-light);
  color: var(--color-success);
}

.history-item-status.failed {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.history-item-status.processing {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.history-item-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  min-width: 26px;
  margin-top: 2px;
  border: none;
  border-radius: var(--radius-xs);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.history-item:hover .history-item-delete {
  opacity: 1;
}

.history-item-delete:hover {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

/* ===== Main Wrapper ===== */
.app-main-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100vh;
  overflow: hidden;
}

/* ===== Header ===== */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  padding: 0 20px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.header-menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.header-menu-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.header-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  min-width: 0;
}

.breadcrumb-root {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.breadcrumb-sep {
  color: var(--color-text-muted);
  font-size: 12px;
}

.breadcrumb-current {
  color: var(--color-text);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-task-id {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--color-code-bg);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
}

.task-id-label {
  color: var(--color-text-muted);
  font-size: 11px;
  font-weight: 500;
}

.task-id-value {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--color-primary);
}

.header-status-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  background: var(--color-surface-hover);
  color: var(--color-text-secondary);
}

.header-status-pill.processing {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.header-status-pill.completed {
  background: var(--color-success-light);
  color: var(--color-success);
}

.header-status-pill.failed {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.header-status-pill.processing .status-dot {
  animation: pulse-dot 1.5s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.7); }
}

/* ===== Wizard Bar ===== */
.wizard-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
  height: var(--wizard-height);
  background: var(--color-bg-alt);
  border-bottom: 1px solid var(--color-border);
  gap: 0;
  flex-shrink: 0;
}

.wizard-step {
  display: flex;
  align-items: center;
  position: relative;
  cursor: default;
  user-select: none;
  padding: 8px 0;
}

.wizard-step.clickable {
  cursor: pointer;
}

.wstep-circle {
  width: 28px;
  height: 28px;
  min-width: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  background: var(--color-border);
  color: var(--color-text-muted);
  transition: all var(--transition-base);
  border: 2px solid transparent;
}

.wizard-step.active .wstep-circle {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px var(--color-primary-light);
}

.wizard-step.done .wstep-circle {
  background: var(--color-success-light);
  color: var(--color-success);
  border-color: var(--color-success);
}

.wizard-step.done .wstep-circle svg {
  width: 14px;
  height: 14px;
}

.wstep-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-muted);
  margin-left: 8px;
  margin-right: 24px;
  white-space: nowrap;
  transition: color var(--transition-base);
}

.wizard-step.active .wstep-label {
  color: var(--color-text);
  font-weight: 600;
}

.wizard-step.done .wstep-label {
  color: var(--color-text-secondary);
}

.wstep-connector {
  position: absolute;
  top: 50%;
  left: calc(100% - 20px);
  width: 16px;
  height: 2px;
  background: var(--color-border);
  transform: translateY(-50%);
  border-radius: 2px;
  overflow: hidden;
}

.wstep-connector-fill {
  height: 100%;
  background: var(--color-success);
  border-radius: 2px;
  transition: width var(--transition-base);
}

/* ===== Main Content Area ===== */
.app-main {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
}

.app-main::-webkit-scrollbar {
  width: 6px;
}

.app-main::-webkit-scrollbar-track {
  background: transparent;
}

.app-main::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 3px;
}

.app-main::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-muted);
}

/* ===== Step Views ===== */
.step-view {
  max-width: 880px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 24px 48px;
  animation: step-enter 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  flex: 1;
}

.step-processing {
  max-width: 1080px;
}

.step-results {
  max-width: none;
  padding: 8px 14px 10px;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.step-annotation {
  max-width: none;
  padding: 12px 14px 0;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* Step Bottom Navigation */
.step-bottom-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 0 8px;
  margin-top: auto;
  gap: 12px;
}

.step-bottom-nav--annotation {
  justify-content: space-between;
  padding: 12px 0;
  border-top: 1px solid var(--color-border);
}

.btn-next-step {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 28px;
  font-size: 14px;
  font-weight: 600;
}

.step-nav-hint {
  font-size: 11px;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.step-nav-hint::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-warning, #e8a020);
}

@keyframes step-enter {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-hero {
  text-align: center;
  margin-bottom: 36px;
}

.step-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.step-desc {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

/* ===== Upload Step ===== */
.upload-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.drop-zone {
  width: 100%;
  min-height: 280px;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
  background: var(--color-surface);
  position: relative;
  overflow: hidden;
}

.drop-zone::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, var(--color-primary-light) 0%, transparent 70%);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.drop-zone:hover::before,
.drop-zone.drag-over::before {
  opacity: 0.5;
}

.drop-zone:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
}

.drop-zone.drag-over {
  border-color: var(--color-primary);
  border-style: solid;
  background: var(--color-primary-light);
  box-shadow: var(--shadow-lg);
  transform: scale(1.01);
}

.drop-zone.has-file {
  border-color: var(--color-success);
  border-style: solid;
  background: var(--color-success-light);
}

.drop-zone-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 40px 24px;
  position: relative;
  z-index: 1;
}

.drop-icon-ring {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  color: var(--color-primary);
  margin-bottom: 8px;
  transition: all var(--transition-base);
}

.drop-zone:hover .drop-icon-ring {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.drop-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
}

.drop-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.drop-formats {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.format-badge {
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  background: var(--color-surface-hover);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.drop-hint {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 4px;
}

.drop-zone-file-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 24px;
  position: relative;
  z-index: 1;
}

.file-preview-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-success-light);
  color: var(--color-success);
  border-radius: var(--radius-md);
  margin-bottom: 4px;
}

.drop-file-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.drop-file-size {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-family: var(--font-mono);
}

.drop-file-remove {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: var(--color-danger-light);
  color: var(--color-danger);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.drop-file-remove:hover {
  background: var(--color-danger);
  color: white;
  transform: scale(1.1);
}

.hidden-input {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* ===== Buttons ===== */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: white;
  font-size: 15px;
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: 0 2px 8px rgba(91, 106, 191, 0.25);
  letter-spacing: 0.1px;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(91, 106, 191, 0.35);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(91, 106, 191, 0.2);
}

.btn-primary:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-secondary:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
  border-color: var(--color-text-muted);
}

.btn-start {
  background: var(--color-accent);
  box-shadow: 0 2px 8px rgba(212, 145, 42, 0.3);
}

.btn-start:hover:not(:disabled) {
  background: var(--color-accent-hover);
  box-shadow: 0 4px 16px rgba(212, 145, 42, 0.4);
}

/* ===== Config Step ===== */
.config-layout {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.card-glass {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  padding: 32px;
  box-shadow: var(--shadow-card);
  transition: box-shadow var(--transition-base);
}

.card-glass:hover {
  box-shadow: var(--shadow-md);
}

.config-section {
  margin-bottom: 28px;
}

.config-half {
  flex: 1;
  min-width: 0;
}

.config-row {
  display: flex;
  gap: 24px;
  margin-bottom: 28px;
}

.config-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 12px;
}

.config-label svg {
  color: var(--color-primary);
}

/* Radio Grid */
.radio-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.radio-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  background: var(--color-surface);
  position: relative;
}

.radio-card:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.radio-card.active {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.radio-card input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.radio-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
}

.radio-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.radio-check {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
  border-radius: 50%;
}

/* Select Fields */
.select-field {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: 14px;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--transition-base);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238a99ae' stroke-width='2.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

.select-field:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

/* Toggle Grid */
.toggle-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toggle-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--color-surface);
}

.toggle-card:hover {
  background: var(--color-surface-hover);
}

.toggle-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toggle-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.toggle-desc {
  font-size: 11px;
  color: var(--color-text-muted);
}

.toggle-switch-wrap {
  position: relative;
  width: 44px;
  height: 26px;
  flex-shrink: 0;
}

.toggle-switch {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 1;
}

.toggle-track {
  position: absolute;
  inset: 0;
  background: var(--color-border);
  border-radius: 13px;
  transition: background var(--transition-base);
}

.toggle-track::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: transform var(--transition-base);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.toggle-switch:checked + .toggle-track {
  background: var(--color-primary);
}

.toggle-switch:checked + .toggle-track::after {
  transform: translateX(18px);
}

/* Config Preview */
.config-preview {
  margin-top: 28px;
  padding: 16px;
  background: var(--color-bg-alt);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-light);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.preview-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.preview-count {
  font-size: 11px;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
}

.preview-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.preview-tag {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  background: var(--color-surface);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

/* Config Actions */
.config-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid var(--color-border-light);
}

/* ===== Processing Step ===== */
.processing-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  padding: 40px 32px;
  box-shadow: var(--shadow-card);
}

.processing-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.processing-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: var(--radius-md);
}

.spin {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.processing-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 2px;
}

.processing-filename {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-family: var(--font-mono);
}

.feature-tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 24px;
}

.feature-tag {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-primary);
  background: var(--color-primary-light);
}

/* Stepper */
.stepper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  position: relative;
  padding: 0 8px;
}

.stepper::before {
  content: '';
  position: absolute;
  top: 14px;
  left: 22px;
  right: 22px;
  height: 2px;
  background: var(--color-border);
  z-index: 0;
}

.stepper .step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.stepper .step-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  background: var(--color-border);
  color: var(--color-text-muted);
  border: 2px solid var(--color-bg);
  transition: all var(--transition-base);
}

.stepper .step.active .step-circle {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px var(--color-primary-light);
}

.stepper .step.done .step-circle {
  background: var(--color-success);
  color: white;
  border-color: var(--color-success);
}

.stepper .step-label {
  font-size: 11px;
  color: var(--color-text-muted);
  white-space: nowrap;
  transition: color var(--transition-base);
}

.stepper .step.active .step-label {
  color: var(--color-text);
  font-weight: 600;
}

.stepper .step.done .step-label {
  color: var(--color-text-secondary);
}

/* Progress Bar */
.progress-section {
  margin-bottom: 24px;
}

.progress-bar-wrap {
  position: relative;
  height: 32px;
  display: flex;
  align-items: center;
}

.progress-bubble {
  position: absolute;
  top: -28px;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: white;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 700;
  font-family: var(--font-mono);
  box-shadow: var(--shadow-sm);
  transition: left var(--transition-base);
  white-space: nowrap;
  z-index: 2;
}

.progress-bubble::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid var(--color-primary);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--color-border);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  border-radius: 4px;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.progress-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  animation: shine 2s ease-in-out infinite;
}

@keyframes shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Processing Stats */
.processing-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 20px 0 0;
  border-top: 1px solid var(--color-border-light);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
  font-family: var(--font-mono);
}

.stat-label {
  font-size: 11px;
  color: var(--color-text-muted);
}

.stat-divider {
  width: 1px;
  height: 32px;
  background: var(--color-border);
}

.processing-message {
  margin-top: 20px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  background: var(--color-bg-alt);
  border: 1px solid var(--color-border-light);
}

.processing-stage {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 6px;
}

.processing-message p {
  font-size: 13px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

/* ===== Results Step ===== */
.result-top-bar {
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.result-top-bar.compact {
  margin-bottom: 8px;
  gap: 10px;
}

.result-filename {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 6px;
  letter-spacing: -0.3px;
}

.result-top-bar.compact .result-filename {
  font-size: 14px;
  margin-bottom: 0;
}

.result-params {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.result-top-bar.compact .result-params {
  gap: 4px;
}

.param-badge {
  padding: 3px 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 600;
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.result-top-bar.compact .param-badge {
  padding: 2px 7px;
  font-size: 10px;
}

.workspace-tabs {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-alt);
}

.workspace-tab {
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.workspace-tab:hover {
  color: var(--color-text);
}

.workspace-tab.active {
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-xs);
}

/* Toolbar */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tool-group {
  display: flex;
  gap: 2px;
  padding: 2px;
  background: var(--color-bg-alt);
  border-radius: var(--radius-sm);
}

.tool-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 7px 12px;
  border: none;
  border-radius: var(--radius-xs);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 13px;
  font-family: var(--font-sans);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.tool-btn:hover {
  color: var(--color-text);
  background: var(--color-surface-hover);
}

.tool-btn.active {
  background: var(--color-surface);
  color: var(--color-text);
  font-weight: 600;
  box-shadow: var(--shadow-xs);
}

.tool-sep {
  width: 1px;
  height: 20px;
  background: var(--color-border);
  margin: 0 6px;
}

.btn-reset {
  color: var(--color-danger);
}

.btn-reset:hover {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.btn-mark-run {
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 700;
}

.btn-mark-run:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-mark-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 700;
  border-radius: var(--radius-md);
}

.btn-mark-cta:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Panels Container */
.panels-container {
  display: flex;
  gap: 0;
  flex: 1;
  min-height: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
}

.panels-container.horizontal {
  flex-direction: row;
}

.panels-container.vertical {
  flex-direction: column;
}

.panels-container.pdf-fullscreen .panel-pdf {
  display: flex !important;
}

.panels-container.md-fullscreen .panel-md {
  display: flex !important;
}

.panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
  min-height: 0;
}

.panels-container.horizontal .panel-pdf {
  width: var(--panel-a-pct, 54%);
  flex: 0 0 var(--panel-a-pct, 54%);
}

.panels-container.horizontal .panel-md {
  width: var(--panel-b-pct, 46%);
  flex: 0 0 var(--panel-b-pct, 46%);
}

.panels-container.vertical .panel-pdf {
  height: var(--panel-a-pct, 50%);
  flex: 0 0 var(--panel-a-pct, 50%);
}

.panels-container.vertical .panel-md {
  height: var(--panel-b-pct, 50%);
  flex: 0 0 var(--panel-b-pct, 50%);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: var(--color-bg-alt);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  user-select: none;
  flex-shrink: 0;
}

.panel-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.panel-header-left svg {
  color: var(--color-text-muted);
}

.panel-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.word-count {
  font-size: 11px;
  color: var(--color-text-secondary);
  font-family: var(--font-mono);
}

.panel-hint {
  font-size: 10px;
  color: var(--color-text-muted);
  opacity: 0.6;
}

.panel-body {
  flex: 1;
  overflow: hidden;
  background: #fafbfc;
}

.app-shell.theme-dark .panel-body {
  background: #0f1928;
}

.panel-body.has-error {
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel-error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
  padding: 32px 24px;
  color: var(--color-text-muted);
}

.panel-error-state svg {
  color: var(--color-warning);
  opacity: 0.7;
}

.panel-error-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}

.panel-error-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
  max-width: 280px;
  line-height: 1.5;
}

.panel-loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 24px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.btn-retry {
  margin-top: 8px;
  padding: 7px 18px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 500;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-retry:hover {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.pdf-status-error {
  font-size: 11px;
  color: var(--color-danger);
  font-weight: 600;
}

.pdf-status-loading {
  font-size: 11px;
  color: var(--color-text-muted);
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background: #fff;
}

.md-body {
  overflow-y: auto;
  line-height: 1.8;
  font-size: 14px;
  color: var(--color-text);
}

.md-panel-layout {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  min-height: 100%;
}

.annotation-sidebar {
  background: var(--color-bg-alt);
  overflow-y: auto;
  min-height: 0;
}

.annotation-sidebar::-webkit-scrollbar {
  width: 4px;
}

.annotation-sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.annotation-sidebar::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.annotation-workspace-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 0 0 10px 0;
  margin-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}

.annotation-workspace-copy {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.annotation-workspace-kicker {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.2px;
}

.annotation-workspace-status-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.annotation-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 11px;
  font-weight: 600;
}

.annotation-status-pill::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  opacity: 0.6;
}

.annotation-workspace-tip {
  font-size: 11px;
  color: var(--color-text-muted);
}

.annotation-workspace-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.annotation-workspace-body {
  display: grid;
  grid-template-columns: 240px 280px minmax(0, 1fr);
  flex: 1;
  min-height: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-surface);
}

.annotation-card {
  height: 100%;
  min-height: 0;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.annotation-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}

.annotation-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.2px;
}

.annotation-desc {
  margin-top: 3px;
  font-size: 11px;
  line-height: 1.5;
  color: var(--color-text-muted);
}

.annotation-refresh-btn {
  width: 28px;
  height: 28px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.annotation-refresh-btn:hover:not(:disabled) {
  color: var(--color-primary);
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.annotation-refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.annotation-utility-row {
  display: flex;
  gap: 6px;
}

.annotation-utility-btn {
  flex: 1;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  padding: 7px 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.annotation-utility-btn:hover {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.annotation-settings-section {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  overflow: hidden;
}

.annotation-settings-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border: none;
  background: none;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.annotation-settings-toggle:hover {
  background: var(--color-surface-hover);
}

.annotation-settings-chevron {
  flex-shrink: 0;
  color: var(--color-text-muted);
  transform: rotate(0deg);
  transition: transform var(--transition-base);
}

.annotation-settings-chevron.expanded {
  transform: rotate(90deg);
}

.btn-start-annotation {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 0;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-start-annotation:hover:not(:disabled) {
  background: var(--color-primary-hover);
  box-shadow: 0 4px 14px rgba(91, 106, 191, 0.35);
}

.btn-start-annotation:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.annotation-rule-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.annotation-rule-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.annotation-rule-item:hover {
  border-color: var(--color-border);
  background: var(--color-surface-hover);
  box-shadow: var(--shadow-xs);
}

.annotation-rule-item.disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.annotation-rule-item input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  margin-top: 2px;
  border: 2px solid var(--color-border);
  border-radius: 3px;
  background: var(--color-surface);
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--transition-fast);
  position: relative;
}

.annotation-rule-item input[type="checkbox"]:checked {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.annotation-rule-item input[type="checkbox"]:checked::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 5px;
  height: 8px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.annotation-rule-item:has(input:checked) {
  border-color: var(--color-primary-soft);
  background: var(--color-primary-light);
}

.annotation-rule-content {
  flex: 1;
  min-width: 0;
}

.annotation-rule-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.annotation-rule-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.annotation-rule-count {
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: var(--radius-full);
  background: var(--color-border-light);
  color: var(--color-text-secondary);
  font-size: 10px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.annotation-rule-item:has(input:checked) .annotation-rule-count {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.annotation-rule-desc {
  margin-top: 3px;
  font-size: 11px;
  line-height: 1.5;
  color: var(--color-text-muted);
}

/* ── Preview area & snippet navigator ── */

.annotation-preview-area {
  display: contents;
}

/* ── Middle Column: Snippet List ── */

.annotation-snippet-column {
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: var(--color-bg-alt);
  border-right: 1px solid var(--color-border);
}

.snippet-column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;
}

.snippet-column-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.snippet-column-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.2px;
  white-space: nowrap;
}

.snippet-column-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 7px;
  border-radius: var(--radius-full);
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 11px;
  font-weight: 700;
  font-family: var(--font-mono);
  line-height: 1;
}

.snippet-column-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.snippet-column-nav-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.snippet-column-nav-btn:hover:not(:disabled) {
  color: var(--color-primary);
  border-color: var(--color-primary-soft);
  background: var(--color-primary-light);
}

.snippet-column-nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.snippet-column-position {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  min-width: 52px;
  text-align: center;
}

.snippet-column-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.snippet-column-list::-webkit-scrollbar {
  width: 4px;
}

.snippet-column-list::-webkit-scrollbar-track {
  background: transparent;
}

.snippet-column-list::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.annotation-snippet-column-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
  padding: 16px;
  background: var(--color-bg-alt);
  border-right: 1px solid var(--color-border);
}

/* ── Snippet Cards ── */

.annotation-snippet-card {
  width: 100%;
  padding: 8px 10px;
  text-align: left;
  border: 1px solid var(--color-border-light);
  border-left: 3px solid var(--color-primary);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.annotation-snippet-card:hover {
  border-color: var(--color-primary-soft);
  border-left-color: var(--color-primary-hover);
  box-shadow: var(--shadow-sm);
  transform: translateX(2px);
}

.annotation-snippet-card.active {
  border-color: var(--color-primary-soft);
  border-left-color: var(--color-primary);
  background: var(--color-primary-light);
  box-shadow: 0 0 0 2px var(--color-primary-soft);
}

.annotation-snippet-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.snippet-color-bar {
  width: 4px;
  min-width: 4px;
  height: 18px;
  border-radius: 2px;
  margin-right: 8px;
  flex-shrink: 0;
}

.annotation-snippet-rule {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.3px;
}

.annotation-snippet-idx {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
}

.snippet-source-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: var(--radius-sm);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.4px;
  flex-shrink: 0;
}
.snippet-source-tag.source-rule {
  background: #e8f0fe;
  color: #1a73e8;
}
.snippet-source-tag.source-model {
  background: #fce8e6;
  color: #d93025;
}

.annotation-snippet-text {
  font-size: 12px;
  line-height: 1.55;
  color: var(--color-text);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.annotation-snippet-context {
  font-size: 11px;
  line-height: 1.45;
  color: var(--color-text-muted);
  margin-top: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.annotation-snippet-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}

.annotation-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 7px;
  border-radius: var(--radius-full);
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-size: 10px;
  font-weight: 600;
}

.annotation-empty-state {
  padding: 16px;
  text-align: center;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 12px;
  line-height: 1.6;
}

.annotation-empty-state.error {
  color: var(--color-danger);
  background: var(--color-danger-light);
}

/* ── Scan animation ── */

.annotation-highlight.annotation-pending {
  opacity: 0;
}

.annotation-highlight.annotation-glowing {
  filter: brightness(1.25) saturate(1.15);
  transition: filter 0.25s ease;
}

.annotation-highlight.annotation-revealed {
  animation: annotation-pop 0.45s ease-out forwards;
}

@keyframes annotation-pop {
  0% { opacity: 0; transform: scale(1.14); filter: brightness(1.8); }
  50% { opacity: 1; transform: scale(1.02); filter: brightness(1.1); }
  100% { opacity: 1; transform: scale(1); filter: brightness(1); }
}

.annotation-scan-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 4px;
  background:
    linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.6) 15%, rgba(99, 102, 241, 0.95) 50%, rgba(59, 130, 246, 0.6) 85%, transparent 100%);
  box-shadow:
    0 0 20px rgba(59, 130, 246, 0.55),
    0 0 50px rgba(99, 102, 241, 0.3),
    0 -6px 12px rgba(59, 130, 246, 0.12),
    0 6px 12px rgba(59, 130, 246, 0.12);
  pointer-events: none;
  z-index: 10;
  border-radius: 2px;
}

.annotation-scan-line::before {
  content: '';
  position: absolute;
  top: -20px;
  left: 0;
  right: 0;
  height: 44px;
  background: linear-gradient(to bottom,
    transparent 0%,
    rgba(99, 102, 241, 0.06) 30%,
    rgba(59, 130, 246, 0.1) 50%,
    rgba(99, 102, 241, 0.06) 70%,
    transparent 100%
  );
  pointer-events: none;
}

.annotation-scan-cursor {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  background: #fff;
  border-radius: 50%;
  box-shadow:
    0 0 8px #fff,
    0 0 18px rgba(99, 102, 241, 0.9),
    0 0 30px rgba(59, 130, 246, 0.6),
    0 0 50px rgba(99, 102, 241, 0.4);
  animation: scan-cursor-pulse 0.8s ease-in-out infinite;
  pointer-events: none;
}

@keyframes scan-cursor-pulse {
  0%, 100% { box-shadow: 0 0 8px #fff, 0 0 18px rgba(99, 102, 241, 0.9), 0 0 30px rgba(59, 130, 246, 0.6), 0 0 50px rgba(99, 102, 241, 0.4); }
  50% { box-shadow: 0 0 12px #fff, 0 0 25px rgba(99, 102, 241, 1), 0 0 40px rgba(59, 130, 246, 0.8), 0 0 65px rgba(99, 102, 241, 0.55); }
}

.annotation-preview-panel {
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-surface);
}

.annotation-preview-header {
  cursor: default;
  background: var(--color-surface);
  border-bottom-color: var(--color-border);
}

.annotation-preview-body {
  position: relative;
  min-height: 0;
  background: #fafbfc;
}

.app-shell.theme-dark .annotation-preview-body {
  background: #0f1928;
}

.md-content-wrap {
  min-width: 0;
  padding: 18px 20px;
}

.review-md-content,
.annotation-md-content {
  min-height: 100%;
}

.md-body::-webkit-scrollbar {
  width: 5px;
}

.md-body::-webkit-scrollbar-track {
  background: transparent;
}

.md-body::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 3px;
}

.md-body h1,
.md-body h2,
.md-body h3,
.md-body h4 {
  margin-top: 1.4em;
  margin-bottom: 0.5em;
  font-weight: 700;
  line-height: 1.3;
  color: var(--color-text);
}

.md-body h1 { font-size: 1.5em; border-bottom: 1px solid var(--color-border); padding-bottom: 0.3em; }
.md-body h2 { font-size: 1.3em; }
.md-body h3 { font-size: 1.1em; }

.md-body p {
  margin-bottom: 0.8em;
}

.md-body code {
  font-family: var(--font-mono);
  font-size: 0.88em;
  padding: 2px 6px;
  border-radius: 4px;
  background: var(--color-code-bg);
  color: var(--color-primary);
}

.md-body pre {
  margin: 1em 0;
  padding: 16px;
  border-radius: var(--radius-sm);
  background: var(--color-code-bg);
  overflow-x: auto;
  border: 1px solid var(--color-border);
}

.md-body pre code {
  padding: 0;
  background: none;
  color: var(--color-text);
  font-size: 13px;
}

.md-body blockquote {
  margin: 1em 0;
  padding: 8px 16px;
  border-left: 3px solid var(--color-primary);
  background: var(--color-primary-light);
  border-radius: 0 var(--radius-xs) var(--radius-xs) 0;
  color: var(--color-text-secondary);
}

.md-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 13px;
}

.md-body th,
.md-body td {
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  text-align: left;
}

.md-body th {
  background: var(--color-bg-alt);
  font-weight: 600;
  color: var(--color-text);
}

.md-body img {
  max-width: 100%;
  border-radius: var(--radius-sm);
  margin: 1em 0;
}

.md-body a {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.md-body ul,
.md-body ol {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.md-body li {
  margin-bottom: 0.3em;
}

.md-error {
  color: var(--color-danger);
  text-align: center;
  padding: 40px;
  font-size: 14px;
}

/* Contenteditable editing indicator */
.md-editing {
  outline: 2px solid var(--color-primary);
  outline-offset: -2px;
  border-radius: var(--radius-xs);
  box-shadow: 0 0 0 6px var(--color-primary-light);
  cursor: text;
}

.md-editing:focus {
  outline-color: var(--color-accent);
  box-shadow: 0 0 0 6px var(--color-accent-light);
}

.annotation-highlight {
  padding: 0 4px;
  border-radius: 4px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
  border-bottom: 2px solid transparent;
}

.annotation-highlight-focus {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 5px;
  animation: annotation-pulse 1.4s ease;
}

@keyframes annotation-pulse {
  0% { box-shadow: 0 0 0 0 rgba(91, 106, 191, 0.45); transform: scale(1); }
  50% { box-shadow: 0 0 0 10px rgba(91, 106, 191, 0); transform: scale(1.04); }
  100% { box-shadow: 0 0 0 0 rgba(91, 106, 191, 0); transform: scale(1); }
}

.btn-edit {
  color: var(--color-accent);
}

.btn-edit:hover {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.btn-save {
  color: var(--color-success);
}

.btn-save:hover:not(:disabled) {
  background: var(--color-success-light);
  color: var(--color-success);
}

.btn-save:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.btn-cancel-edit {
  color: var(--color-danger);
}

.btn-cancel-edit:hover {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

/* Panel Divider */
.panel-divider {
  flex-shrink: 0;
  background: var(--color-border);
  cursor: col-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition-fast);
  z-index: 10;
}

.panels-container.horizontal .panel-divider {
  width: 6px;
  cursor: col-resize;
}

.panels-container.vertical .panel-divider {
  height: 6px;
  cursor: row-resize;
}

.panel-divider:hover {
  background: var(--color-primary);
}

.divider-handle {
  width: 3px;
  height: 32px;
  border-radius: 2px;
  background: var(--color-text-muted);
  opacity: 0.4;
  transition: all var(--transition-fast);
}

.panel-divider:hover .divider-handle {
  opacity: 1;
  background: white;
  width: 3px;
}

.panels-container.vertical .divider-handle {
  width: 32px;
  height: 3px;
}

/* ===== Toast Notifications ===== */
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 10000;
  display: flex;
  flex-direction: column-reverse;
  gap: 10px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: var(--radius-md);
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  pointer-events: all;
  max-width: 380px;
  backdrop-filter: blur(12px);
}

.toast.success {
  border-color: var(--color-success);
  background: var(--color-success-light);
  color: #065f46;
}

.app-shell.theme-dark .toast.success {
  color: var(--color-success);
}

.toast.error {
  border-color: var(--color-danger);
  background: var(--color-danger-light);
  color: #991b1b;
}

.app-shell.theme-dark .toast.error {
  color: var(--color-danger);
}

.toast-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast.success .toast-icon {
  color: var(--color-success);
}

.toast.error .toast-icon {
  color: var(--color-danger);
}

.toast.info .toast-icon {
  color: var(--color-primary);
}

.toast-msg {
  line-height: 1.4;
}

/* Toast Transitions */
.toast-enter-active {
  animation: toast-in 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-leave-active {
  animation: toast-out 0.25s cubic-bezier(0.4, 0, 1, 1);
}

.toast-move {
  transition: transform 0.3s ease;
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateX(40px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes toast-out {
  from {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateX(20px) scale(0.85);
  }
}

/* Fade Scale Transition */
.fade-scale-enter-active {
  animation: fade-scale-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-scale-leave-active {
  animation: fade-scale-out 0.2s cubic-bezier(0.4, 0, 1, 1);
}

@keyframes fade-scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fade-scale-out {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* ===== Responsive Design ===== */
@media (max-width: 768px) {
  .app-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 200;
    transform: translateX(-100%);
    box-shadow: var(--shadow-xl);
  }

  .app-sidebar:not(.collapsed) {
    transform: translateX(0);
  }

  .app-sidebar.collapsed {
    transform: translateX(-100%);
  }

  .app-header {
    padding: 0 12px;
  }

  .header-breadcrumb {
    display: none;
  }

  .wizard-bar {
    padding: 0 8px;
    overflow-x: auto;
  }

  .wstep-label {
    font-size: 11px;
    margin-right: 12px;
  }

  .step-view {
    padding: 20px 12px 40px;
  }

  .step-models {
    padding: 16px 12px;
  }

  .step-results,
  .step-annotation {
    padding: 12px 10px 20px;
  }

  .step-title {
    font-size: 22px;
  }

  .step-desc {
    font-size: 13px;
  }

  .config-row {
    flex-direction: column;
    gap: 12px;
  }

  .card-glass {
    padding: 20px;
  }

  .processing-card {
    padding: 24px 16px;
  }

  .processing-stats {
    gap: 16px;
  }

  .panels-container {
    height: calc(100vh - 188px);
    min-height: 300px;
    flex-direction: column !important;
  }

  .panels-container.horizontal .panel {
    width: 100%;
    height: 50%;
    flex: 1;
  }

  .panels-container.horizontal .panel-divider {
    width: 100%;
    height: 6px;
    cursor: row-resize;
  }

  .panels-container.horizontal .divider-handle {
    width: 32px;
    height: 3px;
  }

  .toolbar {
    padding: 8px 10px;
    gap: 6px;
  }

  .tool-btn {
    padding: 6px 8px;
    font-size: 12px;
  }

  .md-body {
    font-size: 13px;
  }

  .annotation-workspace-toolbar,
  .annotation-workspace-actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .annotation-workspace-body {
    grid-template-columns: 1fr;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  .annotation-sidebar {
    max-height: 36vh;
  }

  .annotation-snippet-column {
    max-height: 36vh;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }

  .annotation-snippet-column-empty {
    max-height: 20vh;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }

  .md-content-wrap {
    padding: 14px 16px;
  }

  .toast-container {
    bottom: 12px;
    right: 12px;
    left: 12px;
  }

  .toast {
    max-width: 100%;
  }

  .result-top-bar {
    flex-direction: column;
  }

  .workspace-tabs {
    width: 100%;
    justify-content: stretch;
  }

  .workspace-tab {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .wstep-label {
    display: none;
  }

  .wstep-connector {
    left: calc(100% - 8px);
    width: 12px;
  }

  .drop-zone {
    min-height: 220px;
  }

  .btn-primary {
    padding: 10px 20px;
    font-size: 14px;
  }

  .btn-secondary {
    padding: 10px 16px;
    font-size: 13px;
  }

  .radio-card {
    padding: 10px 12px;
  }

  .toggle-card {
    padding: 10px 12px;
  }
}

/* Confirm Dialog */
.confirm-overlay {
  position: fixed;
  inset: 0;
  z-index: 20000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-overlay);
  backdrop-filter: blur(4px);
}

.confirm-dialog {
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  max-width: 380px;
  width: calc(100% - 40px);
  box-shadow: var(--shadow-xl);
  text-align: center;
  animation: dialog-in 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes dialog-in {
  from { opacity: 0; transform: scale(0.92) translateY(8px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.confirm-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-warning-light);
  color: var(--color-warning);
  margin: 0 auto 16px;
}

.confirm-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 8px;
}

.confirm-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: 24px;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-confirm-cancel {
  padding: 10px 24px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-confirm-cancel:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.btn-confirm-delete {
  padding: 10px 24px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-danger);
  color: white;
  font-size: 14px;
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-confirm-delete:hover {
  background: #dc2626;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.fade-enter-active {
  animation: fade-in 0.2s ease;
}

.fade-leave-active {
  animation: fade-out 0.15s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-out {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* Print styles */
@media print {
  .app-sidebar,
  .app-header,
  .wizard-bar,
  .toolbar,
  .toast-container,
  .panel-header,
  .panel-divider {
    display: none !important;
  }

  .app-main {
    overflow: visible;
    height: auto;
  }

  .panel-body {
    overflow: visible;
  }

  .md-body {
    padding: 0;
  }
}

/* ── Top nav tabs ── */
.breadcrumb-tab {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}
.breadcrumb-tab:hover { color: var(--color-text); background: var(--color-surface-hover); }
.breadcrumb-tab.active { color: var(--color-primary); font-weight: 700; background: var(--color-primary-light); }

/* ── Sidebar nav item active state ── */
.nav-item-models.active { background: var(--color-primary-light); color: var(--color-primary); }
.models-empty { text-align: center; padding: 48px; color: var(--color-text-muted); font-size: 14px; }

/* ── Annotation card tabs ── */
.annotation-card-tabs { display: flex; gap: 2px; padding: 2px; background: var(--color-border-light); border-radius: var(--radius-sm); margin-bottom: 4px; }
.annotation-card-tab { flex: 1; padding: 6px 0; border: none; background: transparent; color: var(--color-text-muted); font-size: 12px; font-weight: 600; border-radius: 4px; cursor: pointer; transition: all var(--transition-fast); }
.annotation-card-tab.active { background: var(--color-surface); color: var(--color-primary); box-shadow: var(--shadow-xs); }

/* ── Model annotation panel ── */
.annotation-model-panel { display: flex; flex-direction: column; gap: 12px; padding-top: 4px; }
.annotation-model-label { display: block; font-size: 12px; font-weight: 600; color: var(--color-text-secondary); margin-bottom: 4px; }
.annotation-model-divider { display: flex; align-items: center; gap: 12px; color: var(--color-text-muted); font-size: 11px; }
.annotation-model-divider::before, .annotation-model-divider::after { content: ''; flex: 1; height: 1px; background: var(--color-border); }

/* ── 置信度滑块卡片 ── */
.conf-slider-card {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.conf-slider-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.conf-slider-card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
}
.conf-slider-card-title svg {
  flex-shrink: 0;
  color: var(--color-accent);
}
.conf-slider-badge {
  font-size: 12px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  white-space: nowrap;
  transition: background 0.2s, color 0.2s;
}
.conf-badge-high { background: rgba(16,185,129,0.15); color: #10b981; }
.conf-badge-mid { background: rgba(245,158,11,0.15); color: #f59e0b; }
.conf-badge-low { background: rgba(239,68,68,0.12); color: #ef4444; }

/* 轨道包裹：在原生 range 下方叠加渐变色条 */
.conf-slider-track-wrap {
  position: relative;
  height: 24px;
  display: flex;
  align-items: center;
}
.conf-slider-gradient {
  position: absolute;
  left: 0; right: 0; top: 50%;
  transform: translateY(-50%);
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #ef4444 0%, #f59e0b 40%, #eab308 60%, #22c55e 90%, #10b981 100%);
  pointer-events: none;
  overflow: hidden;
}
.conf-slider-gradient-fill {
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: calc(100% - var(--conf-pct, 50%));
  background: var(--color-bg-subtle);
  opacity: 0.5;
  transition: width 0.15s ease;
}
.conf-slider {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
  outline: none;
}
.conf-slider::-webkit-slider-runnable-track {
  height: 6px;
  border-radius: 3px;
  background: transparent;
}
.conf-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid var(--color-accent);
  box-shadow: 0 1px 4px rgba(0,0,0,0.15), 0 0 0 3px rgba(99,102,241,0.15);
  cursor: pointer;
  margin-top: -6px;
  transition: box-shadow 0.15s;
}
.conf-slider::-webkit-slider-thumb:hover {
  box-shadow: 0 1px 6px rgba(0,0,0,0.2), 0 0 0 5px rgba(99,102,241,0.2);
}
.conf-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid var(--color-accent);
  box-shadow: 0 1px 4px rgba(0,0,0,0.15), 0 0 0 3px rgba(99,102,241,0.15);
  cursor: pointer;
}

/* 快速预设按钮 */
.conf-slider-presets {
  display: flex;
  gap: 6px;
}
.conf-preset-btn {
  flex: 1;
  padding: 4px 0;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-bg);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all 0.15s;
}
.conf-preset-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
  background: rgba(99,102,241,0.06);
}
.conf-preset-btn.active {
  border-color: var(--color-accent);
  background: rgba(99,102,241,0.12);
  color: var(--color-accent);
}

/* 置信度徽标（命中片段卡片中） */
.snippet-conf-badge { font-size: 10px; padding: 1px 5px; border-radius: 4px; font-weight: 600; }
.conf-high { background: rgba(16,185,129,0.15); color: #10b981; }
.conf-mid { background: rgba(245,158,11,0.15); color: #f59e0b; }
.conf-low { background: rgba(239,68,68,0.12); color: #ef4444; }

/* ── 快速训练弹窗已移除 ── */

/* ── 模型管理页面：左右分栏布局 ── */
.step-models {
  max-width: none;
  width: 100%;
  margin: 0;
  padding: 20px 24px;
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
.models-split-layout {
  display: flex;
  gap: 20px;
  align-items: stretch;
  flex: 1;
  min-height: 0;
}

/* 左侧面板：已训练模型列表 */
.models-left-panel {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
}
.models-left-header {
  display: flex; align-items: center; gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}
.models-left-title { font-size: 16px; font-weight: 600; color: var(--color-text); }
.models-left-count { font-size: 12px; color: var(--color-text-muted); background: var(--color-bg); padding: 2px 8px; border-radius: 12px; }
.models-left-body { flex: 1; overflow-y: auto; padding: 16px; min-height: 0; }

/* 右侧面板：训练新模型 */
.models-right-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
}
.models-right-header {
  display: flex; align-items: center; gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}
.models-right-title { font-size: 16px; font-weight: 600; color: var(--color-text); }
.models-right-body { flex: 1; overflow: hidden; padding: 16px 20px 5px; display: flex; flex-direction: column; gap: 14px; min-height: 0; }

/* 模型卡片列表 */
.models-card-list { display: flex; flex-direction: column; gap: 12px; }
.models-card {
  background: var(--color-bg-subtle);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-light);
  padding: 14px 16px;
  transition: border-color var(--transition-fast);
}
.models-card:hover { border-color: var(--color-primary); }
.models-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.model-name-cell { font-weight: 600; color: var(--color-text); font-size: 14px; }
.models-card-count { font-size: 12px; color: var(--color-text-muted); background: var(--color-bg-subtle); padding: 1px 8px; border-radius: 10px; }
.models-card-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px; }
.model-label-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; background: var(--color-primary-light); color: var(--color-primary); font-size: 11px; font-weight: 500; }
.models-card-bottom { display: flex; justify-content: space-between; align-items: center; }
.model-time-cell { color: var(--color-text-muted); font-size: 12px; white-space: nowrap; }
.model-actions-cell { display: flex; gap: 8px; }

/* 按钮 */
.btn-sm.btn-download { padding: 4px 12px; border: 1px solid var(--color-border); border-radius: 6px; background: var(--color-surface); color: var(--color-text-secondary); font-size: 12px; cursor: pointer; transition: all var(--transition-fast); }
.btn-sm.btn-download:hover { border-color: var(--color-primary); color: var(--color-primary); background: var(--color-primary-light); }
.btn-sm.btn-danger-text { padding: 4px 12px; border: none; border-radius: 6px; background: none; color: var(--color-text-muted); font-size: 12px; cursor: pointer; transition: color var(--transition-fast); }
.btn-sm.btn-danger-text:hover { color: var(--color-danger); }

/* 空状态 */
.models-empty { text-align: center; padding: 32px 16px; color: var(--color-text-muted); font-size: 14px; }

/* 训练表单：文件上传 + 模型名称 */
.train-top-row { display: flex; gap: 16px; align-items: stretch; }
.train-file-upload {
  flex: 1;
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: border-color var(--transition-fast);
  background: var(--color-bg-subtle);
  min-height: 52px;
}
.train-file-upload:hover { border-color: var(--color-primary); }
.train-file-upload.has-file { border-style: solid; border-color: var(--color-primary); background: var(--color-primary-light); }
.train-file-icon { flex-shrink: 0; color: var(--color-text-muted); }
.train-file-upload:hover .train-file-icon { color: var(--color-primary); }
.train-file-text { flex: 1; min-width: 0; }
.train-file-placeholder { color: var(--color-text-muted); font-size: 13px; }
.train-file-name { font-weight: 500; color: var(--color-text); font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block; }
.train-file-remove { flex-shrink: 0; padding: 4px; background: none; border: none; color: var(--color-text-muted); cursor: pointer; }
.train-file-remove:hover { color: var(--color-danger); }
.train-name-input { width: 200px; flex-shrink: 0; }
.train-name-input .config-label { display: block; margin-bottom: 6px; font-size: 12px; font-weight: 500; color: var(--color-text-secondary); }
.train-name-input .select-field { width: 100%; }

/* 超参数网格 */
.train-params-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.train-param-item .config-label { display: block; margin-bottom: 6px; font-size: 12px; font-weight: 500; color: var(--color-text-secondary); }
.train-param-item .select-field { width: 100%; }

/* 隐藏文件输入 */
.hidden-input { display: none !important; }

/* 开始训练按钮 */
.train-actions { display: flex; gap: 12px; margin-top: 8px; }
.btn-train-start {
  width: 100%;
  padding: 12px 20px;
  border: none;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #6366f1, #818cf8);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  transition: opacity var(--transition-fast), transform var(--transition-fast);
}
.btn-train-start:hover:not(:disabled) { opacity: 0.92; transform: translateY(-1px); }
.btn-train-start:disabled { opacity: 0.4; cursor: not-allowed; }

/* 训练进度区域 */
.train-progress-area {
  margin-top: 4px;
  padding: 16px;
  background: var(--color-bg-subtle);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}
.train-progress-header { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.train-progress-title { font-weight: 600; font-size: 15px; color: var(--color-text); }
.train-status-msg { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 8px; }
.train-val-bar {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 10px; margin-bottom: 10px;
  background: rgba(139,92,246,0.08); border-radius: 6px;
  border: 1px solid rgba(139,92,246,0.18);
}
.train-val-label { font-size: 11px; font-weight: 600; color: #8b5cf6; text-transform: uppercase; }
.train-val-metric { font-size: 12px; color: var(--color-text); font-weight: 500; font-variant-numeric: tabular-nums; }
.train-val-sep { color: var(--color-border); font-size: 10px; }
.train-progress-bar-wrap { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.train-progress-bar { flex: 1; height: 8px; background: var(--color-border-light); border-radius: 4px; overflow: hidden; }
.train-progress-bar-fill { height: 100%; background: var(--color-primary); border-radius: 4px; transition: width 0.3s ease; }
.train-progress-pct { font-size: 13px; font-weight: 600; color: var(--color-primary); min-width: 40px; text-align: right; }

/* 图表网格 */
.train-charts-grid { display: flex; flex-direction: column; gap: 16px; }
.train-small-charts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }

/* 图表卡片 */
.train-chart-card {
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.train-chart-card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}
.train-chart-card-title { font-size: 12px; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.5px; }
.train-chart-card-value { font-size: 14px; font-weight: 700; color: #10b981; font-variant-numeric: tabular-nums; }
.train-val-red { color: #ef4444; }
.train-val-purple { color: #8b5cf6; }
.train-chart-body { position: relative; padding: 4px; flex: 1; min-height: 0; }
.train-chart-body canvas { width: 100% !important; height: 100% !important; display: block; }
.train-chart-large .train-chart-body { height: 150px; }
.train-chart-sm { height: 90px; }
.train-chart-hint { padding: 2px 10px 4px; font-size: 10px; color: var(--color-text-muted); line-height: 1.4; border-top: 1px solid var(--color-border-light); }

/* Epoch 环形进度 */
.train-epoch-body { display: flex; align-items: center; justify-content: center; padding: 12px; }
.epoch-ring {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.epoch-ring-inner {
  width: 78px;
  height: 78px;
  border-radius: 50%;
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
}
.epoch-ring-value { font-size: 15px; font-weight: 700; color: var(--color-text); font-variant-numeric: tabular-nums; }
.epoch-ring-pct { font-size: 11px; font-weight: 600; color: var(--color-primary); }
.epoch-ring-time { font-size: 10px; color: var(--color-text-muted); margin-top: 2px; }

.train-log-panel {
  margin: 0;
  padding: 8px 12px;
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 1.55;
  color: var(--color-text-secondary);
  background: transparent;
  white-space: pre-wrap;
  word-break: break-all;
  overflow-y: auto;
  height: 100%;
  border: none;
  outline: none;
}
.train-log-panel::-webkit-scrollbar { width: 4px; }
.train-log-panel::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 2px; }

/* 确认对话框 */
.confirm-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); z-index: 1000; display: flex; align-items: center; justify-content: center; }
.confirm-dialog { background: var(--color-surface); border-radius: var(--radius-lg); padding: 28px 32px; max-width: 420px; width: 90%; box-shadow: var(--shadow-xl); }
.confirm-icon { width: 40px; height: 40px; border-radius: 50%; background: var(--color-danger-light); display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; color: var(--color-danger); }
.confirm-title { font-size: 17px; font-weight: 600; color: var(--color-text); text-align: center; margin-bottom: 8px; }
.confirm-desc { font-size: 14px; color: var(--color-text-secondary); text-align: center; line-height: 1.6; margin-bottom: 24px; }
.confirm-actions { display: flex; gap: 12px; justify-content: center; }
.btn-confirm-cancel { padding: 8px 20px; border: 1px solid var(--color-border); border-radius: 8px; background: var(--color-surface); color: var(--color-text-secondary); font-size: 14px; cursor: pointer; }
.btn-confirm-cancel:hover { background: var(--color-bg-subtle); }
.btn-confirm-delete { padding: 8px 20px; border: none; border-radius: 8px; background: var(--color-danger); color: white; font-size: 14px; cursor: pointer; font-weight: 500; }
.btn-confirm-delete:hover { background: var(--color-danger-hover, #c0392b); }

.eval-section {
  margin-top: 12px;
  padding: 14px;
  background: var(--color-bg-subtle);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
}
.eval-section-header {
  display: flex; align-items: center; gap: 8px;
  font-weight: 600; font-size: 15px; color: var(--color-text);
  margin-bottom: 8px;
}
.eval-section-header svg { color: var(--color-primary); }
.eval-form {
  display: flex; gap: 12px; align-items: stretch; margin-bottom: 12px;
}
.eval-file-upload {
  flex: 1; min-height: 42px; padding: 10px 14px;
}
.eval-metrics-row {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
  margin-bottom: 16px;
}
.eval-metric-card {
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-light);
  padding: 14px 16px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.eval-metric-value {
  font-size: 20px; font-weight: 700; color: var(--color-primary);
  font-variant-numeric: tabular-nums;
}
.eval-metric-label {
  font-size: 11px; color: var(--color-text-muted);
  text-transform: uppercase; letter-spacing: 0.5px;
}
.eval-chart-container {
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-light);
  padding: 8px 14px;
}

/* ── 训练表单区域 ── */
.train-form-section { flex-shrink: 0; }

/* ── 模型管理 TAB 按钮 ── */
.models-tab-btn {
  padding: 8px 20px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.models-tab-btn:hover { background: var(--color-surface-hover); color: var(--color-text); }
.models-tab-btn.active { background: var(--color-primary); color: white; font-weight: 600; }

/* ── 模型卡片选中态 ── */
.models-card { cursor: pointer; }
.models-card-selected { border-color: var(--color-primary) !important; background: var(--color-primary-light); }

/* ── 新建模型训练按钮 ── */
.btn-new-model-train {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 13px; font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.btn-new-model-train:hover { background: var(--color-primary-light); color: var(--color-primary); border-color: var(--color-primary); }

/* ── 模型详情视图 ── */
.model-detail-view { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; min-height: 0; }
.model-detail-topbar { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
.model-detail-name { font-weight: 600; font-size: 16px; color: var(--color-text); }
.model-detail-content { display: flex; flex-direction: column; gap: 12px; }
.model-detail-stats { display: flex; gap: 16px; font-size: 13px; color: var(--color-text-secondary); }
.model-detail-charts { display: flex; flex-direction: column; gap: 8px; }
</style>

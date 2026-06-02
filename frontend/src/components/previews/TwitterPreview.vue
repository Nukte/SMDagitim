<template>
  <div class="tw-preview card">
    <div class="tw-frame">
      <!-- Header -->
      <div class="tw-header">
        <div class="tw-avatar"></div>
        <div class="tw-user-info">
          <div class="tw-name-row">
            <span class="tw-name">Kullanıcı Adı</span>
            <span class="tw-verified">✓</span>
          </div>
          <span class="tw-handle">@kullanici · şimdi</span>
        </div>
        <span class="tw-logo">𝕏</span>
      </div>

      <!-- Tweet Content -->
      <div class="tw-content">
        <p class="tw-text">{{ displayText }}</p>
        <span v-if="isOverLimit" class="tw-over-limit">
          ⚠️ {{ postStore.content.length - 280 }} karakter fazla
        </span>
      </div>

      <!-- Hashtags -->
      <div v-if="postStore.hashtags.length" class="tw-hashtags">
        <span v-for="tag in postStore.hashtags" :key="tag" class="tw-hashtag">#{{ tag }}</span>
      </div>

      <!-- Media -->
      <div v-if="firstMedia" class="tw-media">
        <img
          v-if="firstMedia.media_type === 'image'"
          :src="firstMedia.localPreview || firstMedia.public_url"
          alt=""
          class="tw-media-img"
        />
        <div v-else class="tw-media-video">
          <span>▶️</span>
        </div>
      </div>

      <!-- Time -->
      <div class="tw-time">
        {{ currentTime }} · X for Web
      </div>

      <!-- Stats -->
      <div class="tw-stats">
        <span><strong>0</strong> Repost</span>
        <span><strong>0</strong> Alıntı</span>
        <span><strong>0</strong> Beğeni</span>
        <span><strong>0</strong> Görüntüleme</span>
      </div>

      <!-- Actions -->
      <div class="tw-actions">
        <span>💬</span>
        <span>🔄</span>
        <span>🤍</span>
        <span>📊</span>
        <span>📤</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../../stores/post'

const postStore = usePostStore()
const firstMedia = computed(() => postStore.media[0] || null)

const isOverLimit = computed(() => postStore.content.length > 280)

const displayText = computed(() => {
  const text = postStore.content || 'Buraya tweet içeriği gelecek...'
  return text
})

const currentTime = computed(() => {
  const now = new Date()
  return now.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) +
    ' · ' + now.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' })
})
</script>

<style scoped>
.tw-preview { overflow: hidden; }

.tw-frame {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  padding: var(--space-4);
}

.tw-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.tw-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--text-tertiary);
  flex-shrink: 0;
}

.tw-user-info { flex: 1; }

.tw-name-row {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.tw-name {
  font-size: var(--font-size-sm);
  font-weight: 700;
}

.tw-verified {
  background: var(--accent);
  color: white;
  font-size: 10px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.tw-handle {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

.tw-logo {
  font-size: 1.2rem;
  font-weight: 800;
}

.tw-content {
  margin-bottom: var(--space-3);
}

.tw-text {
  font-size: var(--font-size-base);
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.tw-over-limit {
  display: inline-block;
  margin-top: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--error);
  font-weight: 600;
}

.tw-hashtags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-bottom: var(--space-3);
}

.tw-hashtag {
  color: var(--accent);
  font-size: var(--font-size-sm);
}

.tw-media {
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 16/9;
  background: var(--bg-tertiary);
  margin-bottom: var(--space-3);
}

.tw-media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tw-media-video {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
}

.tw-time {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--border);
}

.tw-stats {
  display: flex;
  gap: var(--space-5);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--border);
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

.tw-stats strong {
  color: var(--text-primary);
}

.tw-actions {
  display: flex;
  justify-content: space-around;
  padding-top: var(--space-3);
  font-size: 1.1rem;
}
</style>

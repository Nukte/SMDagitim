<template>
  <div class="fb-preview card">
    <div class="fb-frame">
      <!-- Header -->
      <div class="fb-header">
        <div class="fb-avatar"></div>
        <div class="fb-user-info">
          <span class="fb-name">Sayfa Adı</span>
          <div class="fb-meta">
            <span>Şimdi</span>
            <span>·</span>
            <span>🌐</span>
          </div>
        </div>
        <span class="fb-more">⋯</span>
      </div>

      <!-- Content -->
      <div class="fb-content">
        <p class="fb-text">{{ displayText }}</p>
        <div v-if="postStore.hashtags.length" class="fb-hashtags">
          <span v-for="tag in postStore.hashtags" :key="tag" class="fb-hashtag">#{{ tag }}</span>
        </div>
      </div>

      <!-- Media -->
      <div v-if="firstMedia" class="fb-media">
        <img
          v-if="firstMedia.media_type === 'image'"
          :src="firstMedia.localPreview || firstMedia.public_url"
          alt=""
          class="fb-media-img"
        />
        <div v-else class="fb-media-video">
          <span>▶️</span>
        </div>
      </div>

      <!-- Reactions Bar -->
      <div class="fb-reactions-bar">
        <div class="fb-reactions-icons">
          <span class="fb-reaction-icon">👍</span>
          <span class="fb-reaction-icon">❤️</span>
          <span class="fb-reaction-count">42</span>
        </div>
        <div class="fb-reactions-stats">
          <span>5 yorum</span>
          <span>·</span>
          <span>2 paylaşım</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="fb-actions">
        <button class="fb-action-btn">👍 Beğen</button>
        <button class="fb-action-btn">💬 Yorum Yap</button>
        <button class="fb-action-btn">↗️ Paylaş</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../../stores/post'

const postStore = usePostStore()
const firstMedia = computed(() => postStore.media[0] || null)

const displayText = computed(() => {
  return postStore.content || 'Buraya post içeriği gelecek...'
})
</script>

<style scoped>
.fb-preview { overflow: hidden; }

.fb-frame {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.fb-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
}

.fb-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--facebook);
  flex-shrink: 0;
}

.fb-user-info { flex: 1; }

.fb-name {
  font-size: var(--font-size-sm);
  font-weight: 700;
  display: block;
}

.fb-meta {
  display: flex;
  gap: var(--space-1);
  font-size: 11px;
  color: var(--text-tertiary);
}

.fb-more {
  font-size: 1.2rem;
  color: var(--text-secondary);
}

.fb-content {
  padding: 0 var(--space-4) var(--space-3);
}

.fb-text {
  font-size: var(--font-size-sm);
  line-height: 1.5;
  color: var(--text-primary);
  white-space: pre-wrap;
}

.fb-hashtags {
  margin-top: var(--space-2);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.fb-hashtag {
  color: var(--facebook);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.fb-media {
  aspect-ratio: 16/9;
  background: var(--bg-tertiary);
}

.fb-media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.fb-media-video {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.fb-reactions-bar {
  display: flex;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

.fb-reactions-icons {
  display: flex;
  align-items: center;
  gap: 2px;
}

.fb-reaction-icon { font-size: 14px; }
.fb-reaction-count { margin-left: var(--space-1); }

.fb-reactions-stats {
  display: flex;
  gap: var(--space-1);
}

.fb-actions {
  display: flex;
  border-top: 1px solid var(--border);
  padding: var(--space-1);
}

.fb-action-btn {
  flex: 1;
  padding: var(--space-2);
  font-family: var(--font-sans);
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-secondary);
  background: none;
  border: none;
  border-radius: var(--radius-sm);
  cursor: default;
  transition: background var(--transition-fast);
}
</style>

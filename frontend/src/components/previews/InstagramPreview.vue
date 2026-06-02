<template>
  <div class="ig-preview card">
    <div class="ig-phone-frame">
      <!-- Header -->
      <div class="ig-header">
        <div class="ig-avatar"></div>
        <div class="ig-user-info">
          <span class="ig-username">kullanici_adi</span>
          <span class="ig-location">📍 Konum</span>
        </div>
        <span class="ig-more">⋯</span>
      </div>

      <!-- Media -->
      <div class="ig-media">
        <img
          v-if="firstMedia && firstMedia.media_type === 'image'"
          :src="firstMedia.localPreview || firstMedia.public_url"
          alt="Post preview"
          class="ig-media-img"
        />
        <div v-else-if="firstMedia && firstMedia.media_type === 'video'" class="ig-media-placeholder">
          <span>🎬</span>
          <span>Video</span>
        </div>
        <div v-else class="ig-media-placeholder ig-no-media">
          <span>📷</span>
          <span>Medya yüklenmedi</span>
        </div>

        <!-- Carousel dots -->
        <div v-if="postStore.media.length > 1" class="ig-carousel-dots">
          <span
            v-for="(_, i) in postStore.media"
            :key="i"
            class="ig-dot"
            :class="{ active: i === 0 }"
          ></span>
        </div>
      </div>

      <!-- Actions -->
      <div class="ig-actions">
        <div class="ig-actions-left">
          <span>🤍</span>
          <span>💬</span>
          <span>📤</span>
        </div>
        <span>🔖</span>
      </div>

      <!-- Likes -->
      <div class="ig-likes">1,234 beğenme</div>

      <!-- Caption -->
      <div class="ig-caption">
        <span class="ig-caption-user">kullanici_adi</span>
        <span class="ig-caption-text">{{ displayCaption }}</span>
      </div>

      <!-- Hashtags -->
      <div v-if="postStore.hashtags.length" class="ig-hashtags">
        <span v-for="tag in postStore.hashtags" :key="tag" class="ig-hashtag">#{{ tag }}</span>
      </div>

      <!-- Time -->
      <div class="ig-time">ŞİMDİ</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../../stores/post'

const postStore = usePostStore()

const firstMedia = computed(() => postStore.media[0] || null)

const displayCaption = computed(() => {
  const text = postStore.content || 'Buraya post içeriği gelecek...'
  return text.length > 150 ? text.substring(0, 150) + '... daha fazla' : text
})
</script>

<style scoped>
.ig-preview {
  overflow: hidden;
}

.ig-phone-frame {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

/* Header */
.ig-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
}

.ig-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  flex-shrink: 0;
}

.ig-user-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.ig-username {
  font-size: var(--font-size-sm);
  font-weight: 600;
}

.ig-location {
  font-size: 10px;
  color: var(--text-tertiary);
}

.ig-more {
  font-size: 1.2rem;
  color: var(--text-secondary);
}

/* Media */
.ig-media {
  position: relative;
  aspect-ratio: 1;
  background: var(--bg-tertiary);
}

.ig-media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ig-media-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.ig-media-placeholder span:first-child {
  font-size: 2.5rem;
}

.ig-no-media {
  opacity: 0.5;
}

.ig-carousel-dots {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
}

.ig-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
}

.ig-dot.active {
  background: #3897f0;
}

/* Actions */
.ig-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  font-size: 1.3rem;
}

.ig-actions-left {
  display: flex;
  gap: var(--space-4);
}

/* Likes */
.ig-likes {
  padding: 0 var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: 600;
}

/* Caption */
.ig-caption {
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

.ig-caption-user {
  font-weight: 600;
  margin-right: var(--space-2);
}

.ig-caption-text {
  color: var(--text-secondary);
}

/* Hashtags */
.ig-hashtags {
  padding: 0 var(--space-4) var(--space-2);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.ig-hashtag {
  font-size: var(--font-size-xs);
  color: #3897f0;
  font-weight: 500;
}

/* Time */
.ig-time {
  padding: var(--space-2) var(--space-4) var(--space-4);
  font-size: 10px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>

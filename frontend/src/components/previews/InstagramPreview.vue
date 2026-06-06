<template>
  <div class="ig-preview">
    <div class="ig-phone-frame">
      <!-- Header -->
      <div class="ig-header">
        <div class="ig-avatar-ring">
          <div class="ig-avatar"></div>
        </div>
        <div class="ig-user-info">
          <span class="ig-username">kullanici_adi</span>
          <span class="ig-location">Konum</span>
        </div>
        <button class="ig-more" aria-label="More options">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle cx="6" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="18" cy="12" r="1.5" fill="currentColor"/>
          </svg>
        </button>
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
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
          <span>Video</span>
        </div>
        <div v-else class="ig-media-placeholder ig-no-media">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
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
          <button class="ig-action-btn" aria-label="Like">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </button>
          <button class="ig-action-btn" aria-label="Comment">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
          </button>
          <button class="ig-action-btn" aria-label="Share">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
        <button class="ig-action-btn" aria-label="Save">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
          </svg>
        </button>
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
  border-radius: var(--radius-lg);
  border: 1px solid #dbdbdb;
  background: #ffffff;
}

.ig-phone-frame {
  background: #ffffff;
  overflow: hidden;
}

/* Header */
.ig-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-bottom: 1px solid #efefef;
}

.ig-avatar-ring {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  padding: 2px;
  flex-shrink: 0;
}

.ig-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #c7c7c7;
  border: 2px solid #ffffff;
}

.ig-user-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.ig-username {
  font-size: 13px;
  font-weight: 600;
  color: #262626;
  line-height: 1.2;
}

.ig-location {
  font-size: 11px;
  color: #262626;
  line-height: 1.2;
}

.ig-more {
  background: none;
  border: none;
  color: #262626;
  cursor: default;
  padding: 4px;
  display: flex;
  align-items: center;
}

/* Media */
.ig-media {
  position: relative;
  aspect-ratio: 1;
  background: #fafafa;
}

.ig-media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.ig-media-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  color: #8e8e8e;
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
  transition: background 0.2s;
}

.ig-dot.active {
  background: #0095f6;
}

/* Actions */
.ig-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px 4px;
}

.ig-actions-left {
  display: flex;
  gap: 14px;
}

.ig-action-btn {
  background: none;
  border: none;
  color: #262626;
  cursor: default;
  padding: 2px;
  display: flex;
  align-items: center;
  transition: opacity 0.15s;
}

/* Likes */
.ig-likes {
  padding: 2px 14px 0;
  font-size: 13px;
  font-weight: 600;
  color: #262626;
}

/* Caption */
.ig-caption {
  padding: 4px 14px;
  font-size: 13px;
  line-height: 1.5;
  color: #262626;
}

.ig-caption-user {
  font-weight: 600;
  margin-right: 5px;
  color: #262626;
}

.ig-caption-text {
  color: #262626;
  font-weight: 400;
}

/* Hashtags */
.ig-hashtags {
  padding: 0 14px 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.ig-hashtag {
  font-size: 13px;
  color: #00376b;
  font-weight: 400;
  cursor: default;
}

/* Time */
.ig-time {
  padding: 4px 14px 12px;
  font-size: 10px;
  color: #8e8e8e;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
</style>

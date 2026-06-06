<template>
  <div class="li-preview card">
    <div class="li-frame">
      <div class="li-header">
        <div class="li-avatar"></div>
        <div class="li-user-info">
          <span class="li-name">Profil Adı</span>
          <span class="li-title">Yazılım Geliştirici</span>
          <span class="li-time">Şimdi · 🌐</span>
        </div>
      </div>
      <div class="li-content">
        <p class="li-text">{{ postStore.content || 'LinkedIn post içeriği...' }}</p>
        <div v-if="postStore.hashtags.length" class="li-hashtags">
          <span v-for="tag in postStore.hashtags" :key="tag" class="li-tag">#{{ tag }}</span>
        </div>
      </div>
      <div v-if="postStore.media[0]" class="li-media">
        <img v-if="postStore.media[0].media_type === 'image'" :src="postStore.media[0].localPreview || postStore.media[0].public_url" alt="" />
        <div v-else class="li-vid">▶️</div>
      </div>
      <div class="li-reactions"><span>👍💡❤️ 12</span><span>3 yorum</span></div>
      <div class="li-actions">
        <button>👍 Beğen</button><button>💬 Yorum</button><button>🔄 Paylaş</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { usePostStore } from '../../stores/post'
const postStore = usePostStore()
</script>

<style scoped>
.li-frame { background: #FFFFFF; border-radius: var(--radius-lg); overflow: hidden; }
.li-header { display: flex; gap: var(--space-3); padding: var(--space-4); }
.li-avatar { width: 48px; height: 48px; border-radius: 50%; background: #0A66C2; flex-shrink: 0; }
.li-user-info { display: flex; flex-direction: column; }
.li-name { font-size: var(--font-size-sm); font-weight: 700; }
.li-title, .li-time { font-size: 11px; color: var(--text-tertiary); }
.li-content { padding: 0 var(--space-4) var(--space-3); }
.li-text { font-size: var(--font-size-sm); line-height: 1.6; white-space: pre-wrap; }
.li-hashtags { margin-top: var(--space-2); display: flex; flex-wrap: wrap; gap: var(--space-1); }
.li-tag { color: #0A66C2; font-size: var(--font-size-sm); font-weight: 600; }
.li-media { aspect-ratio: 16/9; background: var(--bg-input); }
.li-media img { width: 100%; height: 100%; object-fit: cover; }
.li-vid { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 3rem; }
.li-reactions { display: flex; justify-content: space-between; padding: var(--space-3) var(--space-4); font-size: var(--font-size-xs); color: var(--text-tertiary); }
.li-actions { display: flex; border-top: 1px solid var(--border); }
.li-actions button { flex: 1; padding: var(--space-3); font-family: var(--font-sans); font-size: var(--font-size-xs); font-weight: 600; color: var(--text-secondary); background: none; border: none; cursor: default; }
</style>

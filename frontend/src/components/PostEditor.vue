<template>
  <div class="post-editor card">
    <h3 class="editor-title">✍️ İçerik</h3>

    <!-- Text Area -->
    <div class="input-group">
      <textarea
        v-model="postStore.content"
        class="input post-textarea"
        placeholder="Post içeriğinizi yazın..."
        :maxlength="postStore.currentMinChars"
      ></textarea>
      <div class="char-counter">
        <span :class="{ 'char-warning': charRatio > 0.9, 'char-danger': charRatio > 0.95 }">
          {{ postStore.content.length }}
        </span>
        / {{ postStore.currentMinChars }}
      </div>
    </div>

    <!-- Hashtags -->
    <div class="input-group">
      <label class="input-label">🏷️ Etiketler</label>
      <div class="hashtag-input-wrapper">
        <div class="hashtag-chips">
          <span
            v-for="(tag, index) in postStore.hashtags"
            :key="index"
            class="hashtag-chip"
          >
            #{{ tag }}
            <button class="chip-remove" @click="removeHashtag(index)">✕</button>
          </span>
        </div>
        <input
          v-model="newHashtag"
          class="input hashtag-input"
          placeholder="Etiket ekle ve Enter'a bas..."
          @keydown.enter.prevent="addHashtag"
          @keydown.space.prevent="addHashtag"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePostStore } from '../stores/post'

const postStore = usePostStore()
const newHashtag = ref('')

const charRatio = computed(() => {
  return postStore.content.length / postStore.currentMinChars
})

function addHashtag() {
  const tag = newHashtag.value.trim().replace(/^#/, '')
  if (tag && !postStore.hashtags.includes(tag)) {
    postStore.hashtags.push(tag)
  }
  newHashtag.value = ''
}

function removeHashtag(index) {
  postStore.hashtags.splice(index, 1)
}
</script>

<style scoped>
.post-editor {
  padding: var(--space-5);
}

.editor-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
}

.post-textarea {
  min-height: 150px;
  resize: vertical;
}

.char-counter {
  text-align: right;
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: var(--space-1);
}

.char-warning { color: var(--warning); }
.char-danger { color: var(--error); font-weight: 600; }

/* ── Hashtags ── */
.hashtag-input-wrapper {
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-2);
  transition: all var(--transition-fast);
}

.hashtag-input-wrapper:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}

.hashtag-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.hashtag-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-3);
  background: var(--accent-subtle);
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 600;
  border-radius: var(--radius-full);
}

.chip-remove {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  font-size: 10px;
  padding: 0 2px;
  opacity: 0.6;
  transition: opacity var(--transition-fast);
}

.chip-remove:hover {
  opacity: 1;
}

.hashtag-input {
  border: none;
  background: transparent;
  padding: var(--space-1) var(--space-2);
  width: 100%;
  font-size: var(--font-size-sm);
}

.hashtag-input:focus {
  box-shadow: none;
  border-color: transparent;
}

.hashtag-chips:empty + .hashtag-input {
  margin-top: 0;
}

.input-group + .input-group {
  margin-top: var(--space-4);
}
</style>

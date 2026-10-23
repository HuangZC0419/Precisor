import test from 'node:test'
import assert from 'node:assert/strict'

import { resolveQuickTrainShortcutIndex } from './quickTrainShortcuts.js'

test('resolveQuickTrainShortcutIndex supports top-row digits', () => {
  assert.equal(resolveQuickTrainShortcutIndex({ key: '1', code: 'Digit1' }), 1)
  assert.equal(resolveQuickTrainShortcutIndex({ key: '9', code: 'Digit9' }), 9)
})

test('resolveQuickTrainShortcutIndex supports numpad digits', () => {
  assert.equal(resolveQuickTrainShortcutIndex({ key: '1', code: 'Numpad1' }), 1)
  assert.equal(resolveQuickTrainShortcutIndex({ key: '5', code: 'Numpad5' }), 5)
})

test('resolveQuickTrainShortcutIndex supports full-width digits', () => {
  assert.equal(resolveQuickTrainShortcutIndex({ key: '１', code: '' }), 1)
  assert.equal(resolveQuickTrainShortcutIndex({ key: '３', code: '' }), 3)
})

test('resolveQuickTrainShortcutIndex supports legacy keyCode fallback', () => {
  assert.equal(resolveQuickTrainShortcutIndex({ key: 'Process', code: '', keyCode: 49 }), 1)
  assert.equal(resolveQuickTrainShortcutIndex({ key: 'Process', code: '', which: 98 }), 2)
})

test('resolveQuickTrainShortcutIndex ignores invalid shortcut keys', () => {
  assert.equal(resolveQuickTrainShortcutIndex({ key: '0', code: 'Digit0' }), null)
  assert.equal(resolveQuickTrainShortcutIndex({ key: 'a', code: 'KeyA' }), null)
  assert.equal(resolveQuickTrainShortcutIndex({ key: '1', code: 'Digit1', ctrlKey: true }), null)
})

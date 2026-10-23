export function resolveQuickTrainShortcutIndex(event) {
  if (!event) return null
  if (event.ctrlKey || event.altKey || event.metaKey) return null

  const key = typeof event.key === 'string' ? event.key.trim() : ''
  if (/^[1-9]$/.test(key)) {
    return Number(key)
  }

  const fullWidthDigits = '１２３４５６７８９'
  const fullWidthIndex = fullWidthDigits.indexOf(key)
  if (fullWidthIndex >= 0) {
    return fullWidthIndex + 1
  }

  const code = typeof event.code === 'string' ? event.code : ''
  const codeMatch = code.match(/^(?:Digit|Numpad)([1-9])$/)
  if (codeMatch) {
    return Number(codeMatch[1])
  }

  const legacyCode = Number(event.keyCode ?? event.which)
  if (legacyCode >= 49 && legacyCode <= 57) {
    return legacyCode - 48
  }
  if (legacyCode >= 97 && legacyCode <= 105) {
    return legacyCode - 96
  }

  return null
}

export function getQuickTrainSelectionText(previewEl, selection = window.getSelection()) {
  if (!previewEl || !selection || selection.isCollapsed || !selection.rangeCount) return ''

  const range = selection.getRangeAt(0)
  const anchorNode = selection.anchorNode
  const focusNode = selection.focusNode
  const commonNode = range.commonAncestorContainer
  const isInsidePreview = [anchorNode, focusNode, commonNode].some(node => node && previewEl.contains(node))

  if (!isInsidePreview) return ''

  return (selection.toString() || '').trim()
}

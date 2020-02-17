import Vue from 'vue'

import {renderComponent} from './lib/vue-helper'

import DocumentUploader from './components/document/document-uploader.vue'

Vue.config.productionTip = false

function createDocumentUploader (element) {
  /* eslint-disable no-new */
  new Vue({
    components: { DocumentUploader },
    render: renderComponent(element, DocumentUploader)
  }).$mount(element)
}

var els = document.querySelectorAll('.document-upload')
for (let i = 0; i < els.length; i += 1) {
  createDocumentUploader(els[i])
}

document.addEventListener('DOMContentLoaded', function () {
  let docUploader = document.querySelector('#document-upload')
  if (docUploader) {
    createDocumentUploader(docUploader)
  }
})

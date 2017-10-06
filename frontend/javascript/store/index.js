import Vue from 'vue'
import Vuex from 'vuex'

import {SET_PUBLICBODY, SET_USER, UPDATE_SUBJECT, UPDATE_BODY,
  UPDATE_FIRST_NAME, UPDATE_LAST_NAME, UPDATE_EMAIL, UPDATE_ADDRESS,
  UPDATE_PRIVATE
} from './mutation_types'

Vue.use(Vuex)

const STEPS = {
  SELECT_PUBLICBODY: 1,
  CONFIRM_PURPOSE: 2,
  WRITE_REQUEST: 3,
  COMPLETE_PROFILE: 4,
  CONFIRM_REQUEST: 5
}

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  state: {
    publicbodies: [],
    user: {},
    step: STEPS.SELECT_PUBLICBODY,
    subject: '',
    body: ''
  },
  getters: {
    publicbody: state => {
      if (state.publicbodies.length > 0) {
        return state.publicbodies[0]
      }
      return null
    },
    user: state => {
      return state.user
    }
  },
  mutations: {
    [SET_PUBLICBODY] (state, publicbody) {
      state.publicbodies = [publicbody]
      state.step = STEPS.WRITE_REQUEST
    },
    [SET_USER] (state, user) {
      state.user = user
    },
    [UPDATE_SUBJECT] (state, subject) {
      state.subject = subject
    },
    [UPDATE_BODY] (state, body) {
      state.body = body
    },
    [UPDATE_FIRST_NAME] (state, firstName) {
      Vue.set(state.user, 'first_name', firstName)
    },
    [UPDATE_LAST_NAME] (state, lastName) {
      Vue.set(state.user, 'last_name', lastName)
    },
    [UPDATE_ADDRESS] (state, address) {
      Vue.set(state.user, 'address', address)
    },
    [UPDATE_EMAIL] (state, email) {
      Vue.set(state.user, 'email', email)
    },
    [UPDATE_PRIVATE] (state, val) {
      Vue.set(state.user, 'private', val)
    }
  },
  strict: debug
})

const AUTH_APP = import.meta.env.VITE_AUTH_APP
const AUTH_USER = import.meta.env.VITE_AUTH_USER
window.BASE_API_URL = window.location.origin.replace(':5173', '');

const OAuth = new (class OAuth {
  EXPIRES_AT_KEY = 'oauth_expires_at';

  /**
   * Getter stored oauth data
   * @param {string} field
   * @return {string}
  **/
  get(field) {
    const oauth = JSON.parse(window.localStorage.getItem('oauth')) ?? {};
    return field ? oauth[field] : oauth;
  }

  /**
   * Setter stored oauth data
   * @param {object} oauth
   * @return {void}
  **/
  set(oauth) {
    window.localStorage.setItem('oauth', JSON.stringify(oauth));
    if (oauth['expires_in']) {
      const nowInMilliseconds = new Date().getTime();
      const expiresInMilliseconds = oauth['expires_in'] * 1000;
      window.localStorage.setItem(this.EXPIRES_AT_KEY, nowInMilliseconds + expiresInMilliseconds);
    } else {
      window.localStorage.removeItem(this.EXPIRES_AT_KEY);
    }
  }

  /**
   * clear stored oauth data
   * @return {void}
  **/
  clear() {
    window.localStorage.removeItem('oauth');
    window.localStorage.removeItem(this.EXPIRES_AT_KEY);
  }

  /**
   * Request oauth data
   * @param {void}
   * @return {object} oauth
  **/
  async request() {
    if (this.OAuth?.get('username')) {
      return await this.refresh();
    }
    return await this.regenerate();
  }

  /**
   * Request oauth data
   * @param {void}
   * @return {object} oauth
  **/
  async regenerate() {
    const expiresAt = Number(window.localStorage.getItem(this.EXPIRES_AT_KEY));
    const nowInMilliseconds = new Date().getTime();
    const notExpired = expiresAt >= nowInMilliseconds;
    let oauth = this.get();
    if (oauth['token_type'] && notExpired) return oauth;

    // refresh token
    const res = await fetch(
      `${window.BASE_API_URL}/admin-oauth/token/`,
      {
        body: 'grant_type=client_credentials&scope=frontend',
        credentials: 'include',
        headers: {
          'Authorization': `Basic ${AUTH_APP}`,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        method: 'POST',
      }
    );
    if (res.status === 200) {
      oauth = await res.json();
      this.set(oauth);
    }
    return oauth;
  }

  /**
   * Request oauth data
   * @param {void}
   * @return {object} oauth
  **/
  async refresh() {
    const expiresAt = Number(window.localStorage.getItem(this.EXPIRES_AT_KEY));
    const nowInMilliseconds = new Date().getTime();
    const notExpired = expiresAt >= nowInMilliseconds;
    let oauth = this.get();
    if (oauth['token_type'] && notExpired) return oauth;

    // refresh token
    const refreshToken = this.OAuth.get('refresh_token');
    const res = await fetch(
      `${window.BASE_API_URL}/admin-oauth/user_token/`,
      {
        body: `grant_type=refresh_token&refresh_token=${encodeURIComponent(refreshToken)}`,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Basic ${AUTH_USER}`,
        },
        method: 'POST',
      }
    );
    if (res.status === 200) {
      oauth = await res.json();
      this.set(oauth);
    }
    return oauth;
  }
})();

export default class Abstract {
  /**
   * Constructor
  **/
  constructor() {
    const err = {
      100: 'Cannot instantiate an abstract class.',
    };

    if (new.target === Abstract) {
      throw new TypeError(err[100]);
    }

    this.constants = {
      API_URL: `${window.BASE_API_URL}/api`,
      VERSION: 'v1',
    };

    this.OAuth = OAuth;
  }

  /**
   * helper to calculate the basic oauth header
   * @param {void}
   * @return {void}
  **/
  header() {
    return {
      'Authorization': `${this.OAuth.get('token_type')} ${this.OAuth.get('access_token')}`,
    };
  }

  /**
   * Hit GET {this.constants.ENDPOINT}/
   * to get object
   * @param {void}
   * @return {array}
  **/
  async get(id) {
    await this.OAuth.request();
    const res = await fetch(
      `${this.constants.ENDPOINT}/${id}/`,
      {
        credentials: 'include',
        headers: {
          ...this.header(),
          'Content-Type': 'application/json',
        },
        method: 'GET',
      }
    );
    return this._handleError(res);
  }

  /**
   * Hit GET {this.constants.ENDPOINT}/
   * to list objects
   * @param {void}
   * @return {array}
  **/
  async list() {
    await this.OAuth.request();
    const res = await fetch(
      `${this.constants.ENDPOINT}/`,
      {
        credentials: 'include',
        headers: {
          ...this.header(),
          'Content-Type': 'application/json',
        },
        method: 'GET',
      }
    );
    return this._handleError(res);
  }

  /**
   * Hit PUT/POST {this.constants.ENDPOINT}/{id}
   * to save obj detail
   * @param {object} obj detail
   * @return {object}
  **/
  async save(obj) {
    await this.OAuth.request();
    let method = 'POST';
    let url = `${this.constants.ENDPOINT}/`;
    if (obj.id) {
      method = 'PATCH';
      url += `${obj.id}/`
      delete(obj.id);
    }
    const res = await fetch(
      url,
      {
        method,
        body: JSON.stringify(obj),
        credentials: 'include',
        headers: {
          ...this.header(),
          'Content-Type': 'application/json',
        },
      }
    );
    return this._handleError(res);
  }

  /**
   * Protected function to handle any error response
   * @param {object} res from an api request
   * @return {object}
  **/
  async _handleError(res) {
    if ([200, 201, 202].includes(res.status)) {
      try {
        return await res.json();
      } catch {
        return { };
      }
    }
    let error = 'API_ERROR';
    try {
      error = await res.json();
    } catch {
      return { error: res.status };
    }
    return { error: typeof Array.isArray(error) ? error[0] : error  };
  }

  /**
   * Helper to update the endpoint if base api url changed
   * @param {void}
   * @return {void}
  **/
  _updateEndpoint() {
    this.constants.ENDPOINT = `${this.constants.API_URL}/${this.constants.VERSION}/${this.resource}`;
  }
}

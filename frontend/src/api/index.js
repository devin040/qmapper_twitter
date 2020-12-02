function getApiEndpoint() {
    if (process.env.NODE_ENV === "prod") {
      // If API endpoint is specified in an environment variable with production deployment
      return process.env.QMAP_API_ENDPOINT;
    } else {
      // Otherwise, use development endpoint
      return "http://localhost:5000";
    }
}

async function requestWrapper({
    path,
    method = "GET",
    data = null
  }) {
    let headers = {};
    if (data != null) {
      headers["Content-Type"] = "application/json";
    }
    
    const response = await fetch(
      `${getApiEndpoint()}${path}`, 
      {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
      }
    );
  
    return {
      success: response.ok,
      data: await response.json()
    };
  }

const apiWrapper = {
    async testMethod() {
        return requestWrapper({
          path: '/',
          method: "GET"
        })
    },

    async getTopUsers() {
      let fetched = await requestWrapper({
        path: '/topusers',
        method: 'GET'
      })

      if (fetched.success) {
        return fetched.data.result
      } else {
        return null
      }
    },

    async getTopTweetUsers() {
      let fetched = await requestWrapper({
        path: '/toptweetusers',
        method: 'GET'
      })

      if (fetched.success) {
        return fetched.data.result
      } else {
        return null
      }
    },

    async getTopTrending() {
      let fetched = await requestWrapper({
        path: '/simpletrending',
        method: 'GET'
      })

      if (fetched.success) {
        return fetched.data.result
      } else {
        return null
      }
    },

    async getTopBetween() {
      let fetched = await requestWrapper({
        path: '/betweeness',
        method: 'GET'
      })

      if (fetched.success) {
        return fetched.data.result
      } else {
        return null
      }
    },

    async getIndegreeDistro() {
        let fetched = await requestWrapper({
            path: "/indegree",
            method: "GET"
        })
        if (fetched.success) {
            return fetched.data.result
        } else {
            return null
        }
    },

    async getOutdegreeDistro() {
        let fetched = await requestWrapper({
            path: "/outdegree",
            method: "GET"
        })
        if (fetched.success) {
            return fetched.data.result
        } else {
            return null
        }
    }


}

export default apiWrapper

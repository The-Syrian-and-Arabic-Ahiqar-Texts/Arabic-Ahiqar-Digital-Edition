module.exports = {
  devServer: {
    proxy: {
      '/ahiqar': {
        target: 'http://127.0.0.1:5000',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/ahiqar': ''
        }
      },
      '/iiif': {
        target: 'http://127.0.0.1:5004',
        public: 'ahiqar.brown-devost.com',
//        changeOrigin: false,
        pathRewrite: {
          '^/iiif': ''
        }
      }
    }
  }
}
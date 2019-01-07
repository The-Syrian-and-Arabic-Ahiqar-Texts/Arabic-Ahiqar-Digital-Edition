module.exports = {
  devServer: {
    proxy: {
//      '/ahiqar': {
//        target: 'http://127.0.0.1:5564',
        //ws: true,
        //changeOrigin: true
//      },
      '^/iiif': {
        target: 'http://127.0.0.1:5004'
      }
    }
  }
}
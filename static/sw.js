importScripts('https://storage.googleapis.com/workbox-cdn/releases/3.1.0/workbox-sw.js');

if (workbox) {
  console.log(`Yay! Workbox is loaded 🎉`);
} else {
  console.log(`Boo! Workbox didn't load 😬`);
}

workbox.precaching.precache([
  {
    url: '/static/bootstrap/css/bootstrap.min.css',
    revision: 'abcd',
  },
  {
    url: '/static/stylish/css/stylish-portfolio.min.css',
    revision: 'abcd',
  },
  {
    url: '/static/images/jpg/bg-masthead-min.jpg',
    revision: 'abcd',
  },
  {
    url: '/static/images/jpg/bg-callout.jpg',
    revision: 'abcd',
  },
  {
    url: '/static/icon/png/objetivo-min.png',
    revision: 'abcd',
  },
  {
    url: '/static/icon/png/mision-min.png',
    revision: 'abcd',
  },
  {
    url: '/static/icon/png/vision-min.png',
    revision: 'abcd',
  },
  {
    url: '/static/icon/png/micro-min.png',
    revision: 'abcd',
  },
  {
    url: '/static/images/jpg/cuadro-1-min.jpg',
    revision: 'abcd',
  },
  {
    url: '/static/images/jpg/cuadro-2-min.jpg',
    revision: 'abcd',
  },
  {
    url: '/static/images/jpg/cuadro-3-min.jpg',
    revision: 'abcd',
  },
  {
    url: '/static/images/jpg/cuadro-4-min.jpg',
    revision: 'abcd',
  },
  {
    url: '/static/plugin/jquery/jquery.min.js',
    revision: 'abcd',
  },
  {
    url: '/static/bootstrap/js/bootstrap.bundle.min.js',
    revision: 'abcd',
  },
  {
    url: '/static/stylish/js/stylish-portfolio.min.js',
    revision: 'abcd',
  }
]);
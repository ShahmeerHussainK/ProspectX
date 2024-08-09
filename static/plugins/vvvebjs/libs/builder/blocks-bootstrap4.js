/*
Copyright 2017 Ziadin Givan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

https://github.com/givanz/Vvvebjs
*/

// Vvveb.BlocksGroup['Bootstrap 4 Snippets'] =
// ["bootstrap4/signin-split", "bootstrap4/slider-header", "bootstrap4/image-gallery", "bootstrap4/video-header", "bootstrap4/about-team", "bootstrap4/portfolio-one-column", "bootstrap4/portfolio-two-column", "bootstrap4/portfolio-three-column", "bootstrap4/portfolio-four-column"];
Vvveb.BlocksGroup['Bootstrap 4 Snippets'] =
    ["bootstrap4/image-gallery", "bootstrap4/video-header", "bootstrap4/about-team", "bootstrap4/testimonial"];

// Vvveb.BlocksGroup['Count Down'] =
    // ["bootstrap4/countdown1"]; //, "bootstrap4/video-header", "bootstrap4/about-team", "bootstrap4/testimonial"];


Vvveb.Blocks.add("bootstrap4/signin-split", {
    name: "Modern Sign In Page with Split Screen Format",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/product.png">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/sign-in-split.jpg",
    html: `
<div class="container-fluid">
  <div class="row no-gutter">
    <div class="d-none d-md-flex col-md-4 col-lg-6 bg-image"></div>
    <div class="col-md-8 col-lg-6">
      <div class="login d-flex align-items-center py-5">
        <div class="container">
          <div class="row">
            <div class="col-md-9 col-lg-8 mx-auto">
              <h3 class="login-heading mb-4">Welcome back!</h3>
              <form>
                <div class="form-label-group">
                  <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
                  <label for="inputEmail">Email address</label>
                </div>

                <div class="form-label-group">
                  <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
                  <label for="inputPassword">Password</label>
                </div>

                <div class="custom-control custom-checkbox mb-3">
                  <input type="checkbox" class="custom-control-input" id="customCheck1">
                  <label class="custom-control-label" for="customCheck1">Remember password</label>
                </div>
                <button class="btn btn-lg btn-primary btn-block btn-login text-uppercase font-weight-bold mb-2" type="submit">Sign in</button>
                <div class="text-center">
                  <a class="small" href="#">Forgot password?</a></div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
<style>
.login,
.image {
  min-height: 100vh;
}

.bg-image {
  background-image: url('https://source.unsplash.com/WEQbe2jBg40/600x1200');
  background-size: cover;
  background-position: center;
}

.login-heading {
  font-weight: 300;
}

.btn-login {
  font-size: 0.9rem;
  letter-spacing: 0.05rem;
  padding: 0.75rem 1rem;
  border-radius: 2rem;
}

.form-label-group {
  position: relative;
  margin-bottom: 1rem;
}

.form-label-group>input,
.form-label-group>label {
  padding: var(--input-padding-y) var(--input-padding-x);
  height: auto;
  border-radius: 2rem;
}

.form-label-group>label {
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  width: 100%;
  margin-bottom: 0;
  line-height: 1.5;
  color: #495057;
  cursor: text;
  /* Match the input under the label */
  border: 1px solid transparent;
  border-radius: .25rem;
  transition: all .1s ease-in-out;
}

.form-label-group input::-webkit-input-placeholder {
  color: transparent;
}

.form-label-group input:-ms-input-placeholder {
  color: transparent;
}

.form-label-group input::-ms-input-placeholder {
  color: transparent;
}

.form-label-group input::-moz-placeholder {
  color: transparent;
}

.form-label-group input::placeholder {
  color: transparent;
}

.form-label-group input:not(:placeholder-shown) {
  padding-top: calc(var(--input-padding-y) + var(--input-padding-y) * (2 / 3));
  padding-bottom: calc(var(--input-padding-y) / 3);
}

.form-label-group input:not(:placeholder-shown)~label {
  padding-top: calc(var(--input-padding-y) / 3);
  padding-bottom: calc(var(--input-padding-y) / 3);
  font-size: 12px;
  color: #777;
}
</style>  
</div>
`,
});

Vvveb.Blocks.add("bootstrap4/image-gallery", {
    name: "Image gallery",
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/thumbnail-gallery.jpg",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/product.png">',
    html: `
<div class="container">

  <h1 class="font-weight-light text-center text-lg-left mt-4 mb-0">Thumbnail Gallery</h1>

  <hr class="mt-2 mb-5">

  <div class="row text-center text-lg-left">

    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/pWkk7iiCoDM/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/aob0ukAYfuI/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/EUfxH-pze7s/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/M185_qYH8vg/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/sesveuG_rNo/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/AvhMzHwiE_0/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/2gYsZUmockw/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/EMSDtjVHdQ8/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/8mUEy0ABdNE/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/G9Rfc1qccH4/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/aJeH0KcFkuc/400x300" alt="">
          </a>
    </div>
    <div class="col-lg-3 col-md-4 col-6">
      <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="https://source.unsplash.com/p2TQ-3Bh3Oo/400x300" alt="">
          </a>
    </div>
  </div>

</div>
`,
});

Vvveb.Blocks.add("bootstrap4/slider-header", {
    name: "Image Slider Header",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/product.png">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/full-slider.jpg",
    html: `
<header class="slider">
  <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
    <ol class="carousel-indicators">
      <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
      <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
      <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
    </ol>
    <div class="carousel-inner" role="listbox">
      <!-- Slide One - Set the background image for this slide in the line below -->
      <div class="carousel-item active" style="background-image: url('https://source.unsplash.com/LAaSoL0LrYs/1920x1080')">
        <div class="carousel-caption d-none d-md-block">
          <h2 class="display-4">First Slide</h2>
          <p class="lead">This is a description for the first slide.</p>
        </div>
      </div>
      <!-- Slide Two - Set the background image for this slide in the line below -->
      <div class="carousel-item" style="background-image: url('https://source.unsplash.com/bF2vsubyHcQ/1920x1080')">
        <div class="carousel-caption d-none d-md-block">
          <h2 class="display-4">Second Slide</h2>
          <p class="lead">This is a description for the second slide.</p>
        </div>
      </div>
      <!-- Slide Three - Set the background image for this slide in the line below -->
      <div class="carousel-item" style="background-image: url('https://source.unsplash.com/szFUQoyvrxM/1920x1080')">
        <div class="carousel-caption d-none d-md-block">
          <h2 class="display-4">Third Slide</h2>
          <p class="lead">This is a description for the third slide.</p>
        </div>
      </div>
    </div>
    <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </a>
    <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="sr-only">Next</span>
        </a>
  </div>
    
<style>
.carousel-item {
  height: 100vh;
  min-height: 350px;
  background: no-repeat center center scroll;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}
</style>  
</header>
`,
});


Vvveb.Blocks.add("bootstrap4/video-header", {
    name: "Video Header",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/image.svg">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/video-header.jpg",
    html: `
<header class="video">
  <video playsinline="playsinline" autoplay="autoplay" muted="muted" loop="loop">
    <source src="https://storage.googleapis.com/coverr-main/mp4/Mt_Baker.mp4" type="video/mp4">
  </video>
</header>

<section class="my-5">
  <div class="container">
    <div class="row">
      <div class="col-md-8 mx-auto">
        <p>The HTML5 video element uses an mp4 video as a source. Change the source video to add in your own background! The header text is vertically centered using flex utilities that are build into Bootstrap 4.</p>
      </div>
    </div>
  </div>
</section>
<style>
header.video {
  position: relative;
  background-color: black;
  height: 75vh;
  min-height: 25rem;
  width: 100%;
  overflow: hidden;
}

header.video video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: 0;
  -ms-transform: translateX(-50%) translateY(-50%);
  -moz-transform: translateX(-50%) translateY(-50%);
  -webkit-transform: translateX(-50%) translateY(-50%);
  transform: translateX(-50%) translateY(-50%);
}

header.video .container {
  position: relative;
  z-index: 2;
}

header.video .overlay {
  /*position: absolute;*/
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: black;
  opacity: 0.5;
  z-index: 1;
}

@media (pointer: coarse) and (hover: none) {
  header {
    background: url('https://source.unsplash.com/XT5OInaElMw/1600x900') black no-repeat center center scroll;
  }
  header video {
    display: none;
  }
}
</style>
`,
});


Vvveb.Blocks.add("bootstrap4/about-team", {
    name: "About and Team Section",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/image.svg">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/about-team.jpg",
    html: `
<header class="bg-primary text-center py-5 mb-4">
  <div class="container">
    <h1 class="font-weight-light text-white">Meet the Team</h1>
  </div>
</header>

<div class="container">
  <div class="row">
    <!-- Team Member 1 -->
    <div class="col-xl-3 col-md-6 mb-4">
      <div class="card border-0 shadow">
        <img src="https://source.unsplash.com/TMgQMXoglsM/500x350" class="card-img-top" alt="...">
        <div class="card-body text-center">
          <h5 class="card-title mb-0">Team Member</h5>
          <div class="card-text text-black-50">Web Developer</div>
        </div>
      </div>
    </div>
    <!-- Team Member 2 -->
    <div class="col-xl-3 col-md-6 mb-4">
      <div class="card border-0 shadow">
        <img src="https://source.unsplash.com/9UVmlIb0wJU/500x350" class="card-img-top" alt="...">
        <div class="card-body text-center">
          <h5 class="card-title mb-0">Team Member</h5>
          <div class="card-text text-black-50">Web Developer</div>
        </div>
      </div>
    </div>
    <!-- Team Member 3 -->
    <div class="col-xl-3 col-md-6 mb-4">
      <div class="card border-0 shadow">
        <img src="https://source.unsplash.com/sNut2MqSmds/500x350" class="card-img-top" alt="...">
        <div class="card-body text-center">
          <h5 class="card-title mb-0">Team Member</h5>
          <div class="card-text text-black-50">Web Developer</div>
        </div>
      </div>
    </div>
    <!-- Team Member 4 -->
    <div class="col-xl-3 col-md-6 mb-4">
      <div class="card border-0 shadow">
        <img src="https://source.unsplash.com/ZI6p3i9SbVU/500x350" class="card-img-top" alt="...">
        <div class="card-body text-center">
          <h5 class="card-title mb-0">Team Member</h5>
          <div class="card-text text-black-50">Web Developer</div>
        </div>
      </div>
    </div>
  </div>
  <!-- /.row -->

</div>
`,
});


Vvveb.Blocks.add("bootstrap4/portfolio-one-column", {
    name: "One Column Portfolio Layout",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/image.svg">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/portfolio-one-column.jpg",
    html: `
    <div class="container">

      <!-- Page Heading -->
      <h1 class="my-4">Page Heading
        <small>Secondary Text</small>
      </h1>

      <!-- Project One -->
      <div class="row">
        <div class="col-md-7">
          <a href="#">
            <img class="img-fluid rounded mb-3 mb-md-0" src="http://placehold.it/700x300" alt="">
          </a>
        </div>
        <div class="col-md-5">
          <h3>Project One</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laudantium veniam exercitationem expedita laborum at voluptate. Labore, voluptates totam at aut nemo deserunt rem magni pariatur quos perspiciatis atque eveniet unde.</p>
          <a class="btn btn-primary" href="#">View Project</a>
        </div>
      </div>
      <!-- /.row -->

      <hr>

      <!-- Project Two -->
      <div class="row">
        <div class="col-md-7">
          <a href="#">
            <img class="img-fluid rounded mb-3 mb-md-0" src="http://placehold.it/700x300" alt="">
          </a>
        </div>
        <div class="col-md-5">
          <h3>Project Two</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ut, odit velit cumque vero doloremque repellendus distinctio maiores rem expedita a nam vitae modi quidem similique ducimus! Velit, esse totam tempore.</p>
          <a class="btn btn-primary" href="#">View Project</a>
        </div>
      </div>
      <!-- /.row -->

      <hr>

      <!-- Project Three -->
      <div class="row">
        <div class="col-md-7">
          <a href="#">
            <img class="img-fluid rounded mb-3 mb-md-0" src="http://placehold.it/700x300" alt="">
          </a>
        </div>
        <div class="col-md-5">
          <h3>Project Three</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Omnis, temporibus, dolores, at, praesentium ut unde repudiandae voluptatum sit ab debitis suscipit fugiat natus velit excepturi amet commodi deleniti alias possimus!</p>
          <a class="btn btn-primary" href="#">View Project</a>
        </div>
      </div>
      <!-- /.row -->

      <hr>

      <!-- Project Four -->
      <div class="row">

        <div class="col-md-7">
          <a href="#">
            <img class="img-fluid rounded mb-3 mb-md-0" src="http://placehold.it/700x300" alt="">
          </a>
        </div>
        <div class="col-md-5">
          <h3>Project Four</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Explicabo, quidem, consectetur, officia rem officiis illum aliquam perspiciatis aspernatur quod modi hic nemo qui soluta aut eius fugit quam in suscipit?</p>
          <a class="btn btn-primary" href="#">View Project</a>
        </div>
      </div>
      <!-- /.row -->

      <hr>

      <!-- Pagination -->
      <ul class="pagination justify-content-center">
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#">1</a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#">2</a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#">3</a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
        </li>
      </ul>

    </div>
`,
});


Vvveb.Blocks.add("bootstrap4/portfolio-two-column", {
    name: "Two Column Portfolio Layout",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/image.svg">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/portfolio-one-column.jpg",
    html: `
<div class="container">

  <!-- Page Heading -->
  <h1 class="my-4">Page Heading
    <small>Secondary Text</small>
  </h1>

  <div class="row">
    <div class="col-lg-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project One</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Two</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit aliquam aperiam nulla perferendis dolor nobis numquam, rem expedita, aliquid optio, alias illum eaque. Non magni, voluptates quae, necessitatibus unde temporibus.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Three</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Four</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit aliquam aperiam nulla perferendis dolor nobis numquam, rem expedita, aliquid optio, alias illum eaque. Non magni, voluptates quae, necessitatibus unde temporibus.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Five</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Six</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit aliquam aperiam nulla perferendis dolor nobis numquam, rem expedita, aliquid optio, alias illum eaque. Non magni, voluptates quae, necessitatibus unde temporibus.</p>
        </div>
      </div>
    </div>
  </div>
  <!-- /.row -->

  <!-- Pagination -->
  <ul class="pagination justify-content-center">
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">1</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">2</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">3</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
    </li>
  </ul>

</div>
`,
});

Vvveb.Blocks.add("bootstrap4/portfolio-three-column", {
    name: "Three Column Portfolio Layout",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/image.svg">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/portfolio-three-column.jpg",
    html: `
<div class="container">

  <!-- Page Heading -->
  <h1 class="my-4">Page Heading
    <small>Secondary Text</small>
  </h1>

  <div class="row">
    <div class="col-lg-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project One</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet numquam aspernatur eum quasi sapiente nesciunt? Voluptatibus sit, repellat sequi itaque deserunt, dolores in, nesciunt, illum tempora ex quae? Nihil, dolorem!</p>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Two</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Three</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quos quisquam, error quod sed cumque, odio distinctio velit nostrum temporibus necessitatibus et facere atque iure perspiciatis mollitia recusandae vero vel quam!</p>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Four</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Five</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Six</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Itaque earum nostrum suscipit ducimus nihil provident, perferendis rem illo, voluptate atque, sit eius in voluptates, nemo repellat fugiat excepturi! Nemo, esse.</p>
        </div>
      </div>
    </div>
  </div>
  <!-- /.row -->

  <!-- Pagination -->
  <ul class="pagination justify-content-center">
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">1</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">2</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">3</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
    </li>
  </ul>

</div>
`,
});


Vvveb.Blocks.add("bootstrap4/portfolio-four-column", {
    name: "Four Column Portfolio Layout",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/image.svg">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/portfolio-four-column.jpg",
    html: `
<div class="container">

  <!-- Page Heading -->
  <h1 class="my-4">Page Heading
    <small>Secondary Text</small>
  </h1>

  <div class="row">
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project One</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet numquam aspernatur eum quasi sapiente nesciunt? Voluptatibus sit, repellat sequi itaque deserunt, dolores in, nesciunt, illum tempora ex quae? Nihil, dolorem!</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Two</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Three</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quos quisquam, error quod sed cumque, odio distinctio velit nostrum temporibus necessitatibus et facere atque iure perspiciatis mollitia recusandae vero vel quam!</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Four</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Five</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Six</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Itaque earum nostrum suscipit ducimus nihil provident, perferendis rem illo, voluptate atque, sit eius in voluptates, nemo repellat fugiat excepturi! Nemo, esse.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Seven</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p>
        </div>
      </div>
    </div>
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <div class="card h-100">
        <a href="#"><img class="card-img-top" src="http://placehold.it/700x400" alt=""></a>
        <div class="card-body">
          <h4 class="card-title">
            <a href="#">Project Eight</a>
          </h4>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eius adipisci dicta dignissimos neque animi ea, veritatis, provident hic consequatur ut esse! Commodi ea consequatur accusantium, beatae qui deserunt tenetur ipsa.</p>
        </div>
      </div>
    </div>
  </div>
  <!-- /.row -->

  <!-- Pagination -->
  <ul class="pagination justify-content-center">
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">1</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">2</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#">3</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
    </li>
  </ul>

</div>
`,
});

if (site_name === "XCanvas") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-1.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial1.PNG">',
        html: "<div class=\"section parallax dark\" style=\"background-image: url('/static/xsite_template/all_templates/xsite_template_one/images/slider/3.jpg'); padding: 120px 0;\" data-bottom-top=\"background-position:0px 0px;\" data-top-bottom=\"background-position:0px -600px;\">\n" +
            "\n" +
            "                <div class=\"fslider testimonial testimonial-full\" data-arrows=\"false\" style=\"z-index: 2;\">\n" +
            "                    <div id=\"testimonial_class\" class=\"testimonial_class\">\n" +
            "                        <div class=\"slider-wrap\">\n" +
            "                            <div class=\"slide\">\n" +
            "\n" +
            "                                <div class=\"testi-content\">\n" +
            "                                    <p id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                    <div class=\"testi-meta\">\n" +
            "                                        <span id=\"testi_1_person_name\">Person 1</span>\n" +
            "                                        <span id=\"testi_1_company_name\">Argon Tech</span>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                                <div class=\"slide\">\n" +
            "\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_2_person_name\">Person 2</span>\n" +
            "                                            <span id=\"testi_2_company_name\">Argon Tech 2</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                                <div class=\"slide\">\n" +
            "\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_3_person_name\">Person 3</span>\n" +
            "                                            <span id=\"testi_3_company_name\">Argon Tech 3</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "\n" +
            "                <div class=\"video-wrap\" style=\"z-index: 1;\">\n" +
            "                    <div class=\"video-overlay\" style=\"background: rgba(55,80,31,0.9);\"></div>\n" +
            "                </div>\n" +
            "\n" +
            "            </div>",
    });
} else if (site_name === "Violet") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-2.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial.PNG">',
        html: "<section class=\"testimonial-area pt-4 pb-4\" id=\"testimonial\">\n" +
            "    <div class=\"shape-1\"><img src=\"/static/xsite_template/all_templates/xsite_template_two/assets/img/shape/08.png\" alt=\"\">\n" +
            "    </div>\n" +
            "    <div class=\"shape-2\"><img src=\"/static/xsite_template/all_templates/xsite_template_two/assets/img/shape/09.png\" alt=\"\">\n" +
            "    </div>\n" +
            "    <div class=\"container\">\n" +
            "        <div class=\"row justify-content-center\">\n" +
            "            <div class=\"col-lg-10\">\n" +
            "                <div class=\"section-title \">\n" +
            "                    <!-- section title -->\n" +
            "                    <span class=\"subtitle\">Testimonial</span>\n" +
            "                    <h3 class=\"title extra\">What People Say</h3>\n" +
            "                </div><!-- //. section title -->\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"row\">\n" +
            "            <div class=\"col-lg-12\">\n" +
            "                <div class=\"testimonial-carousel\" id=\"testimonials\">\n" +
            "\n" +
            "                    <div class=\"single-testimonial-item\">\n" +
            "                        <!-- single testimonial item -->\n" +
            "                        <img src=\"/static/xsite_template/all_templates/xsite_template_two/assets/img/testimonial/001.png\" alt=\"\">\n" +
            "                        <div class=\"hover\">\n" +
            "                            <!-- hover -->\n" +
            "                            <div class=\"hover-inner\">\n" +
            "                                <div class=\"icon\"><i class=\"fa fa-quote-left\"></i></div>\n" +
            "                                <p id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                <div class=\"author-meta\">\n" +
            "                                    <h4 id=\"testi_1_person_name\" class=\"name\">Person 1</h4>\n" +
            "                                    <span id=\"testi_1_company_name\" class=\"post\">Argon Tech</span>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div><!-- //. hover -->\n" +
            "                    </div><!-- //. single testimonial item -->\n" +
            "                    <div class=\"single-testimonial-item\">\n" +
            "                        <!-- single testimonial item -->\n" +
            "                        <img src=\"/static/xsite_template/all_templates/xsite_template_two/assets/img/testimonial/002.png\" alt=\"\">\n" +
            "                        <div class=\"hover\">\n" +
            "                            <!-- hover -->\n" +
            "                            <div class=\"hover-inner\">\n" +
            "                                <div class=\"icon\"><i class=\"fa fa-quote-left\"></i></div>\n" +
            "                                <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                <div class=\"author-meta\">\n" +
            "                                    <h4 id=\"testi_2_person_name\" class=\"name\">Person 2</h4>\n" +
            "                                    <span id=\"testi_2_company_name\" class=\"post\">Argon Tech 2</span>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div><!-- //. hover -->\n" +
            "                    </div><!-- //. single testimonial item -->\n" +
            "                    <div class=\"single-testimonial-item\">\n" +
            "                        <!-- single testimonial item -->\n" +
            "                        <img src=\"/static/xsite_template/all_templates/xsite_template_two/assets/img/testimonial/002.png\" alt=\"\">\n" +
            "                        <div class=\"hover\">\n" +
            "                            <!-- hover -->\n" +
            "                            <div class=\"hover-inner\">\n" +
            "                                <div class=\"icon\"><i class=\"fa fa-quote-left\"></i></div>\n" +
            "                                <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                <div class=\"author-meta\">\n" +
            "                                    <h4 id=\"testi_3_person_name\" class=\"name\">Person 3</h4>\n" +
            "                                    <span id=\"testi_3_company_name\" class=\"post\">Argon Tech 3</span>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div><!-- //. hover -->\n" +
            "                    </div><!-- //. single testimonial item -->\n" +
            "                </div>\n" +
            "            </div>\n" +
            "        </div>\n" +
            "    </div>\n" +
            "</section>",
    });
} else if (site_name === "XBrownStone") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-3.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial3.PNG">',
        html: "<div class=\"section mt-0\" id=\"testimonails\" style=\"background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/3.jpg') no-repeat top center; background-size: cover; padding: 80px 0 70px;\">\n" +
            "                <div class=\"container\">\n" +
            "                    <div class=\"heading-block nobottomborder center\">\n" +
            "                        <div class=\"badge badge-pill badge-default\">Testimonials</div>\n" +
            "                        <h3 class=\"nott ls0\">What Clients Says</h3>\n" +
            "                    </div>\n" +
            "\n" +
            "                    <div id=\"oc-testi\" class=\"oc-testi testimonials-carousel carousel-widget clearfix\" data-margin=\"0\" data-pagi=\"true\" data-loop=\"true\" data-center=\"true\" data-autoplay=\"5000\" data-items-sm=\"1\" data-items-md=\"2\" data-items-xl=\"3\">\n" +
            "\n" +
            "                        <div class=\"oc-item\">\n" +
            "                            <div class=\"testimonial\">\n" +
            "                                <div class=\"testi-image\">\n" +
            "                                    <a href=\"#\"><img src=\"/static/xsite_template/all_templates/xsite_template_three/images/avatar.png\" alt=\"Customer Testimonails\"></a>\n" +
            "                                </div>\n" +
            "                                <div class=\"testi-content\">\n" +
            "                                    <p id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                    <div class=\"testi-meta\">\n" +
            "                                        <span id=\"testi_1_person_name\">Person 1</span>\n" +
            "                                        <span id=\"testi_1_company_name\">Argon Tech</span>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                        <div class=\"oc-item\">\n" +
            "                                <div class=\"testimonial\">\n" +
            "                                    <div class=\"testi-image\">\n" +
            "                                        <a href=\"#\"><img src=\"/static/xsite_template/all_templates/xsite_template_three/images/avatar.png\" alt=\"Customer Testimonails\"></a>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_2_person_name\">Person 2</span>\n" +
            "                                            <span id=\"testi_2_company_name\">Argon Tech 2</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"oc-item\">\n" +
            "                                <div class=\"testimonial\">\n" +
            "                                    <div class=\"testi-image\">\n" +
            "                                        <a href=\"#\"><img src=\"/static/xsite_template/all_templates/xsite_template_three/images/avatar.png\" alt=\"Customer Testimonails\"></a>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_3_person_name\">Person 3</span>\n" +
            "                                            <span id=\"testi_3_company_name\">Argon Tech 3</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>",
    });
} else if (site_name === "Modernistic") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-4.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial4.PNG">',
        html: "<div class=\"section section-details mb-0 bg-white\" style=\"padding: 80px 0 80px;\" id=\"testimonials\">\n" +
            "                <div class=\"container clearfix\">\n" +
            "                    <div class=\"row\">\n" +
            "                        <div class=\"col-md-3 px-4 mb-2\">\n" +
            "                            \n" +
            "                             \n" +
            "                             \n" +
            "                        </div>\n" +
            "                        <div class=\"col-md-6 px-4 mb-5 mb-md-0\">\n" +
            "                            <h4 class=\"t500 mb-3\">Testimonials</h4>\n" +
            "                            <div id=\"oc-testi\" class=\"oc-testi testimonials-carousel carousel-widget\" data-margin=\"0\" data-nav=\"false\" data-pagi=\"false\" data-items=\"1\" data-autoplay=\"6000\" data-loop=\"true\" data-animate-in=\"fadeIn\" data-animate-out=\"fadeOut\">\n" +
            "\n" +
            "                                <div class=\"oc-item\">\n" +
            "                                    <div class=\"testimonial nobg noshadow noborder p-0\">\n" +
            "                                        <div class=\"testi-content\">\n" +
            "                                            <p id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                            <div class=\"testi-meta ls1\" id=\"testi_1_person_name\">Person 1</div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                                    <div class=\"oc-item\">\n" +
            "                                        <div class=\"testimonial nobg noshadow noborder p-0\">\n" +
            "                                            <div class=\"testi-content\">\n" +
            "                                                <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                                <div class=\"testi-meta ls1\" id=\"testi_2_person_name\">Person 2</div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"oc-item\">\n" +
            "                                        <div class=\"testimonial nobg noshadow noborder p-0\">\n" +
            "                                            <div class=\"testi-content\">\n" +
            "                                                <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                                <div class=\"testi-meta ls1\" id=\"testi_3_person_name\">Person 3</div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>",
    });
} else if (site_name === "Dark") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-5.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial5.PNG">',
        html: "<div class=\"section nomargin nopadding clearfix\" style=\"padding: 100px 0\" id=\"testimonials\">\n" +
            "                <div class=\"row align-items-stretch clearfix\">\n" +
            "\n" +
            "\n" +
            "                    <div class=\" offset-lg-3 col-md-8 col-lg-6 mb-4 mt-4\">\n" +
            "                        <!-- <h3 class=\"mb-3 text-center\">Testimonials</h3> -->\n" +
            "                        <h2 class=\"font-primary nott text-center\">Testimonials</h2>\n" +
            "                        <div id=\"oc-testi\" class=\"oc-testi testimonials-carousel carousel-widget text-center\" data-margin=\"0\" data-items=\"1\" data-loop=\"true\" data-autoplay=\"5500\" data-pagi=\"false\">\n" +
            "\n" +
            "                            <div class=\"oc-item\">\n" +
            "                                <div class=\"testimonial noborder noshadow \">\n" +
            "\n" +
            "                                    <div class=\"testi-content border-bottom pb-4\">\n" +
            "                                        <p style=\"font-style: normal\" id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"mt-2\">\n" +
            "                                            <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"far fa-star\"></i>\n" +
            "                                        </div>\n" +
            "                                        <div class=\"testi-meta\"><span id=\"testi_1_person_name\">Person 1</span><span id=\"testi_1_company_name\">Argon Tech</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"oc-item\">\n" +
            "                                <div class=\"testimonial noborder noshadow\">\n" +
            "\n" +
            "                                    <div class=\"testi-content border-bottom pb-4\">\n" +
            "                                        <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"mt-2\">\n" +
            "                                            <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star-half\"></i>\n" +
            "                                        </div>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_2_person_name\">Person 2</span>\n" +
            "                                            <span id=\"testi_2_company_name\">Argon Tech 2</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "\n" +
            "                            </div>\n" +
            "                            <div class=\"oc-item\">\n" +
            "                                <div class=\"testimonial noborder noshadow\">\n" +
            "\n" +
            "                                    <div class=\"testi-content border-bottom pb-4\">\n" +
            "                                        <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"mt-2\">\n" +
            "                                            <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i> <i class=\"fa fa-star\"></i>\n" +
            "                                        </div>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_3_person_name\">Person 3</span>\n" +
            "                                            <span id=\"testi_3_company_name\">Argon Tech 3</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "\n" +
            "                            </div>\n" +
            "\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>",
    });
} else if (site_name === "Business") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-6.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial6.PNG">',
        html: "<div class=\"col-lg-7 offset-lg-1 col-md-12 mt-4\">\n" +
            "                        <h4 class=\"dark \">Testimonials</h4>\n" +
            "                        <div class=\"fslider testimonial\" data-animation=\"slide\" data-arrows=\"false\">\n" +
            "                            <div id=\"testimonial_class\" class=\"testimonial_class\">\n" +
            "                                <div class=\"slider-wrap\">\n" +
            "                                    <div class=\"slide\">\n" +
            "                                        <div class=\"testimonial noborder noshadow\">\n" +
            "                                            <div class=\"testi-content\">\n" +
            "                                                <p class=\"bottommargin-sm font-primary\" id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                                <div class=\"testi-meta\">\n" +
            "                                                    <span id=\"testi_1_person_name\">Person 1</span>\n" +
            "                                                    <span id=\"testi_1_company_name\">Argon Tech</span>\n" +
            "                                                    <div class=\"testimonials-rating\">\n" +
            "                                                        <i class=\"fa fa-star\"></i>\n" +
            "                                                        <i class=\"fa fa-star\"></i>\n" +
            "                                                        <i class=\"fa fa-star\"></i>\n" +
            "                                                        <i class=\"fa fa-star\"></i>\n" +
            "                                                        <i class=\"fa fa-star\"></i>\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                        <div class=\"slide\">\n" +
            "                                            <div class=\"testimonial noborder noshadow\">\n" +
            "                                                <div class=\"testi-content\">\n" +
            "                                                    <p class=\"bottommargin-sm font-primary\" id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                                    <div class=\"testi-meta\">\n" +
            "                                                         <span id=\"testi_2_person_name\">Person 2</span>\n" +
            "                                                         <span id=\"testi_2_company_name\">Argon Tech 2</span>\n" +
            "                                                        <div class=\"testimonials-rating\">\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                        </div>\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                        <div class=\"slide\">\n" +
            "                                            <div class=\"testimonial noborder noshadow\">\n" +
            "                                                <div class=\"testi-content\">\n" +
            "                                                    <p class=\"bottommargin-sm font-primary\" id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                                    <div class=\"testi-meta\">\n" +
            "                                                        <span id=\"testi_3_person_name\">Person 3</span>\n" +
            "                                                        <span id=\"testi_3_company_name\">Argon Tech 3</span>\n" +
            "                                                        <div class=\"testimonials-rating\">\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                            <i class=\"fa fa-star\"></i>\n" +
            "                                                        </div>\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>",
    });
} else if (site_name === "Educational") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-7.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial7.PNG">',
        html: "<div id=\"Testimonials\" class=\"section mt-0\" style=\"background: url('/static/xsite_template/all_templates/xsite_template_seven/images/icon-pattern.jpg') no-repeat top center; background-size: cover; padding: 80px 0 70px;\">\n" +
            "                <div class=\"container\">\n" +
            "                    <div class=\"heading-block nobottomborder center\">\n" +
            "                        <h3 class=\"nott ls0\">What Clients Says</h3>\n" +
            "                    </div>\n" +
            "\n" +
            "                    <div id=\"oc-testi\" class=\"oc-testi testimonials-carousel carousel-widget clearfix\" data-margin=\"0\" data-pagi=\"true\" data-loop=\"true\" data-center=\"true\" data-autoplay=\"5000\" data-items-sm=\"1\" data-items-md=\"2\" data-items-xl=\"3\">\n" +
            "\n" +
            "                        <div class=\"oc-item\">\n" +
            "                            <div class=\"testimonial\">\n" +
            "                                <div class=\"testi-content\">\n" +
            "                                    <p id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                    <div class=\"testi-meta\">\n" +
            "                                        <span id=\"testi_1_person_name\">Person 1</span>\n" +
            "                                        <span id=\"testi_1_company_name\">Argon Tech</span>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                        <div class=\"oc-item\">\n" +
            "                            <div class=\"testimonial\">\n" +
            "                                <div class=\"testi-content\">\n" +
            "                                    <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                    <div class=\"testi-meta\">\n" +
            "                                        <span id=\"testi_2_person_name\">Person 2</span>\n" +
            "                                        <span id=\"testi_2_company_name\">Argon Tech 2</span>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                        <div class=\"oc-item\">\n" +
            "                            <div class=\"testimonial\">\n" +
            "                                <div class=\"testi-content\">\n" +
            "                                    <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                    <div class=\"testi-meta\">\n" +
            "                                        <span id=\"testi_3_person_name\">Person 3</span>\n" +
            "                                        <span id=\"testi_3_company_name\">Argon Tech 3</span>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>",
    });
} else if (site_name === "Vacation") {
    Vvveb.Blocks.add("bootstrap4/testimonial", {
        name: "Testimonial",
        image: "icons/Template-8.jpg",
        dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/testimonial8.PNG">',
        html: "<div class=\"container topmargin pt-4 pb-4 clearfix\" id=\"testimonials\">\n" +
            "                <div class=\"row clearfix pt-1\">\n" +
            "                    <div class=\"col-lg-7\">\n" +
            "                        <div class=\"heading-block nobottomborder topmargin-sm nobottommargin\">\n" +
            "                            <h2 class=\"font-secondary ls1 nott t400\">Testimonials</h2>\n" +
            "                            <span>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptates deserunt\n" +
            "\t\t\t\t\t\t\t\t\tfacere placeat est animi, sunt?</span>\n" +
            "                            <a href=\"#get_a_qoute\" class=\"button button-large button-rounded topmargin-sm noleftmargin banner_button_text btn-danger\">Get Your E-book</a>\n" +
            "                            <div class=\"line line-sm\"></div>\n" +
            "                        </div>\n" +
            "                        <div class=\"row clearfix\">\n" +
            "                            <div class=\"col-md-4\">\n" +
            "                                <div>\n" +
            "                                    <div class=\"counter counter-small color\"><span data-from=\"10\" data-to=\"1136\" data-refresh-interval=\"50\" data-speed=\"1000\"></span>+\n" +
            "                                    </div>\n" +
            "                                    <h5 class=\"color t600 nott notopmargin\" style=\"font-size: 16px;\">Happy Customers\n" +
            "                                    </h5>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "\n" +
            "                            <div class=\"col-md-4\">\n" +
            "                                <div>\n" +
            "                                    <div class=\"counter counter-small\" style=\"color: #22c1c3;\"><span data-from=\"10\" data-to=\"145\" data-refresh-interval=\"50\" data-speed=\"700\"></span>+\n" +
            "                                    </div>\n" +
            "                                    <h5 class=\"t600 nott notopmargin\" style=\"color: #22c1c3; font-size: 16px;\">\n" +
            "                                        Property Sold</h5>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "\n" +
            "                            <div class=\"col-md-4\">\n" +
            "                                <div>\n" +
            "                                    <div class=\"counter counter-small\" style=\"color: #BD3F32;\"><span data-from=\"10\" data-to=\"50\" data-refresh-interval=\"85\" data-speed=\"1200\"></span>+\n" +
            "                                    </div>\n" +
            "                                    <h5 class=\"t600 nott notopmargin\" style=\"color: #BD3F32; font-size: 16px;\">\n" +
            "                                        Professional builders</h5>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "\n" +
            "                    <div class=\"col-lg-5 pb-4\">\n" +
            "                        <div id=\"oc-testi\" class=\"oc-testi testimonials-carousel carousel-widget\" data-nav=\"false\" data-animate-in=\"slideInUp\" data-animate-out=\"slideOutUp\" data-autoplay=\"5000\" data-loop=\"true\" data-stage-padding=\"5\" data-margin=\"10\" data-items-sm=\"1\" data-items-md=\"1\" data-items-xl=\"1\">\n" +
            "\n" +
            "                            <div class=\"oc-item\">\n" +
            "                                <div class=\"testimonial topmargin-sm\">\n" +
            "                                    <div class=\"testi-image\">\n" +
            "                                        <a href=\"#\"><img src=\"data:image/jpeg;base64,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\" alt=\"Customer Testimonails\"></a>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_1_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_1_person_name\">Person 1</span>\n" +
            "                                            <span id=\"testi_1_company_name\">Argon Tech</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"oc-item\">\n" +
            "\n" +
            "                                <div class=\"testimonial topmargin-sm\">\n" +
            "                                    <div class=\"testi-image\">\n" +
            "                                        <a href=\"#\"><img src=\"/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/2.jpg\" alt=\"Customer Testimonails\"></a>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_2_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_2_person_name\">Person 2</span>\n" +
            "                                            <span id=\"testi_2_company_name\">Argon Tech 2</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "\n" +
            "                            </div>\n" +
            "                            <div class=\"oc-item\">\n" +
            "\n" +
            "                                <div class=\"testimonial topmargin-sm\">\n" +
            "                                    <div class=\"testi-image\">\n" +
            "                                        <a href=\"#\"><img src=\"/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/3.jpg\" alt=\"Customer Testimonails\"></a>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"testi-content\">\n" +
            "                                        <p id=\"testi_3_text\">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>\n" +
            "                                        <div class=\"testi-meta\">\n" +
            "                                            <span id=\"testi_3_person_name\">Person 3</span>\n" +
            "                                            <span id=\"testi_3_company_name\">Argon Tech 3</span>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "\n" +
            "                </div>\n" +
            "            </div>",
    });
}


Vvveb.Blocks.add("bootstrap4/countdown1", {
    name: "Countdown 1",
    dragHtml: '<img src="' + Vvveb.baseUrl + 'icons/product.png">',
    image: "https://startbootstrap.com/assets/img/screenshots/snippets/sign-in-split.jpg",
    html: `<div class="rounded bg-gradient-1 text-white shadow p-5 text-center mb-5 w-50">
                <p class="mb-4 font-weight-bold text-uppercase">New year's eve in</p>
                <div id="clock" class="countdown-circles d-flex flex-wrap justify-content-center pt-4"></div>
            </div>  
`,
});
from django.db import migrations


def xsite_data_migrations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    # User = apps.get_model('auth', 'User')
    Audience = apps.get_model('xsiteApp', 'Audience')
    MembershipPlan = apps.get_model('xsiteApp', 'MembershipPlan')
    Status = apps.get_model('xsiteApp', 'Status')
    BuyerOptions = apps.get_model('xsiteApp', 'BuyerOptions')
    ListingOptions = apps.get_model('xsiteApp', 'ListingOptions')
    ContentPack = apps.get_model('xsiteApp', 'ContentPack')
    SiteDesign = apps.get_model('xsiteApp', 'SiteDesign')
    SiteCategory = apps.get_model('xsiteApp', 'SiteCategory')

    category = SiteCategory.objects.create(category_name="Real Estate", category_desc="Select your real estate website option.",
                                category_icon="fa fa-synagogue")
    SiteCategory.objects.create(category_name="Educational", category_desc="Select your educational website option.",
                                category_icon="fa fa-book")

    audience_buyer = Audience.objects.create(audience_name="Buyer")
    audience_seller = Audience.objects.create(audience_name="Seller")

    Status.objects.create(status_name="New")
    Status.objects.create(status_name="Follow Up")
    Status.objects.create(status_name="Pending")
    Status.objects.create(status_name="Won")
    Status.objects.create(status_name="Dead")

    BuyerOptions.objects.create(option_name="Commercial")
    BuyerOptions.objects.create(option_name="Investor")
    BuyerOptions.objects.create(option_name="Landlord")
    BuyerOptions.objects.create(option_name="Landlord - Turn Key")
    BuyerOptions.objects.create(option_name="Lease Option")
    BuyerOptions.objects.create(option_name="Owner Finance")
    BuyerOptions.objects.create(option_name="Rehabber")
    BuyerOptions.objects.create(option_name="Renter")
    BuyerOptions.objects.create(option_name="Retail")

    ListingOptions.objects.create(listing_name="Yes")
    ListingOptions.objects.create(listing_name="No")
    ListingOptions.objects.create(listing_name="Will Be Listed Soon")

    MembershipPlan.objects.create(plan="Monthly", billing_amount=47)
    MembershipPlan.objects.create(plan="Yearly", billing_amount=219)

    buyer_content_pack = ContentPack.objects.create(content_pack_name="Buyer's Pack",
                                                    logo="xsite_images/website_logos/xsite_logo.png",
                                                    banner_title="NEED TO SELL YOUR HOUSE?",
                                                    banner_button_text="Get My Offer Now!",
                                                    about_us_title="Little More Detail About Us",
                                                    about_us_desc="We are a house buying company with over 20+ years combined experience working in the housing market to make sure you are getting the best offer for your house. We are committed to making your house selling experience quick and easy! Get your offer today!",
                                                    video_link="https://www.youtube.com/watch?v=NS0txu_Kzl8",
                                                    video_title="HOW FAST DO WE CLOSE?",
                                                    video_desc="We close as fast as you want us to! We process your information as fast as possible, so we can get you an offer within the week! If you decide to accept the offer, we can close within the same week!",
                                                    testi_1_company_name="-",
                                                    testi_1_person_name="KEN C.",
                                                    testi_1_text="They worked hard to close all my liens on my property. They really worked hard to get my property sold. I am a happy camper and appreciate his effort!",

                                                    testi_2_company_name="-",
                                                    testi_2_person_name="VERONICA L.",
                                                    testi_2_text="Our house was damaged by the storms and there was no way we can afford to pay the damages. This company helped us out and we really appreciate the kindness!",

                                                    testi_3_company_name="-",
                                                    testi_3_person_name="MASON T.",
                                                    testi_3_text="I recently was offered a different job in another country and I needed to sell my house fast. This company was able to buy my house for a fair price and I was able to sell quickly!”",

                                                    other_details_title="HOW DO WE CALCULATE YOUR OFFER?",
                                                    other_details_desc="We use the information provided about your house. Two major factors when we calculate our offers are the amount of damage to the house as well as the location of the property.",

                                                    call_to_action_text="Reach Us Now")

    seller_content_pack = ContentPack.objects.create(content_pack_name="Seller's Pack",
                                                     logo="xsite_images/website_logos/xsite_logo.png",
                                                     banner_title="NEED TO BUY A HOUSE?",
                                                     banner_button_text="Get My Offer Now!",
                                                     about_us_title="Little More Detail About Us",
                                                     about_us_desc="We are a house selling company with over 20+ years combined experience working in the housing market to make sure you are getting the best house deals. We are committed to making your house buying experience quick and easy! Get your offer today!",
                                                     video_link="https://www.youtube.com/watch?v=NS0txu_Kzl8",
                                                     video_title="HOW FAST DO WE CLOSE?",
                                                     video_desc="We close as fast as you want us to! We process your information as fast as possible, so we can get you an offer within the week! If you decide to accept the offer, we can close within the same week!",
                                                     testi_1_company_name="-",
                                                     testi_1_person_name="KEN C.",
                                                     testi_1_text="They worked hard to close all my liens on my property. They really worked hard to get my property sold. I am a happy camper and appreciate his effort!",

                                                     testi_2_company_name="-",
                                                     testi_2_person_name="VERONICA L.",
                                                     testi_2_text="Our house was damaged by the storms and there was no way we can afford to pay the damages. This company helped us out and we really appreciate the kindness!",

                                                     testi_3_company_name="-",
                                                     testi_3_person_name="MASON T.",
                                                     testi_3_text="I recently was offered a different job in another country and I needed to sell my house fast. This company was able to buy my house for a fair price and I was able to sell quickly!”",

                                                     other_details_title="HOW DO WE CALCULATE YOUR OFFER?",
                                                     other_details_desc="We use the information provided about your house. Two major factors when we calculate our offers are the amount of damage to the house as well as the location of the property.",

                                                     call_to_action_text="Reach Us Now")

    XCanvas_head = """<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta name="author" content="Xsite"/>
    <title>Xsite</title>

    <!-- Stylesheets
    ============================================= -->
    <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700|Roboto:300,400,500,700"
          rel="stylesheet" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/swiper.css" type="text/css"/>

    <!-- Construction Demo Specific Stylesheet -->
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_one/construction.css"
          type="text/css"/>
    <!-- / -->

    <link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_one/css/fonts.css"
          type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>

    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_one/css/colors.css"
          type="text/css"/>
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">
</head>"""

    XCanvas_body = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <header id="header">

        <div class="container clearfix">


            <!-- Logo
            ============================================= -->
            <div id="logo">
                <a href="#" class="standard-logo"><img
                        src="/media/xsite_images/website_logos/prospectx-logo.png"
                        alt="Canvas Logo"></a>
                <a href="#" class="retina-logo"><img
                        src="/media/xsite_images/website_logos/prospectx-logo.png"
                        alt="Canvas Logo"></a>
            </div><!-- #logo end -->

            <ul class="header-extras">
                <li>
                    <i class="i-plain fa fa-phone nomargin fa-flip-horizontal"></i>
                    <div class="he-text">
                        Call Us
                        <span id="phone">03334455667</span>
                    </div>
                </li>
                <li>
                    <i class="i-plain fa fa-envelope nomargin"></i>
                    <div class="he-text">
                        Email Us
                        <span id="email">support@gmail.com</span>
                    </div>
                </li>
            </ul>

        </div>

    </header><!-- #header end -->
    <!-- Full Page Image Header with Vertically Centered Content -->
    <section class="first_temp_xsite_slider xsite_slider">
        <div class="container h-100">
            <div class="row h-100 align-items-center">
                <div class=" xsite_slider_bg shadow border-custom">
                    <div class="row">

                        <div class="col-sm-12">
                            <div class="border p-3">
                                <h2 id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home
                                    Prices.</h2>
                                <form id="buyer_form" class="nobottommargin" name="template-contactform" method="post">
                                    <div class="form-process"></div>

                                    <div class="col_half mb-2">
                                        <label for="template-contactform-name-buyer">Name <small>*</small></label>
                                        <input type="text"
                                               name="fullname"
                                               id="template-contactform-name-buyer"
                                               class="sm-form-control required"/>
                                    </div>

                                    <div class="col_half col_last mb-2">
                                        <label for="template-contactform-email-buyer">Email <small>*</small></label>
                                        <input type="email"
                                               name="email"
                                               id="template-contactform-email-buyer"
                                               class="required email sm-form-control"/>
                                    </div>

                                    <div class="clear"></div>

                                    <div class="col_half mb-2">
                                        <label for="template-contactform-phone-buyer">Phone<small>*</small></label>
                                        <input type="text" id="template-contactform-phone-buyer"
                                               name="phone"
                                               class="sm-form-control"/>
                                    </div>
                                    <div class="col_half col_last mb-2">
                                        <label for="template-contactform-service-buyer">What are you looking
                                            for?</label>
                                        <select id="template-contactform-service-buyer"
                                                name="what_are_you_looking_for" class="sm-form-control">
                                            <option value="">What are you looking for?</option>
                                        </select>
                                    </div>
                                    <input type="hidden" name="audience" value="Buyer">
                                    <div class="col_full mb-2 pt-2">
                                        <button class="button btn-block button-3d nomargin" type="submit"
                                                name="template-contactform-submit"
                                                id="template-contactform-submit-buyer"
                                                value="submit"> Get Your ebook

                                        </button>
                                    </div>

                                </form>
                                <form id="seller_form" class="nobottommargin" name="template-contactform" method="post">
                                    <div class="form-process"></div>
                                    <input type="hidden" name="audience" value="Seller">
                                    <div class="col_half  mb-2">
                                        <label for="template-contactform-name-seller">Name <small>*</small></label>
                                        <input type="text" id="template-contactform-name-seller"
                                               name="fullname"
                                               class="sm-form-control required"/>
                                    </div>
                                    <div class="col_half col_last mb-2">
                                        <label for="template-contactform-phone-seller">Phone<small>*</small></label>
                                        <input type="text" id="template-contactform-phone-seller"
                                               name="phone"
                                               class="sm-form-control"/>
                                    </div>
                                    <div class="clear"></div>
                                    <div class="col_full col_last  mb-2">
                                        <label for="template-contactform-email-seller">Email
                                            <small>*</small></label>
                                        <input type="email" id="template-contactform-email-seller"
                                               name="email"
                                               class="required email sm-form-control"/>
                                    </div>

                                    <div class="col_full mb-3 pt-3">

                                        <div class="form-check">
                                            <label class="form-check-label">

                                                <input name="immediate_assistance" id="immediate_assistance"
                                                       type="checkbox"
                                                       class="form-check-input" onclick="javascript:ShowFields()">
                                                I
                                                would like
                                                immediate assistance
                                            </label>
                                        </div>
                                    </div>

                                    <div id="immediate_assistance_fields" style="display: none">
                                        <div class="col_half mb-2">
                                            <label for="template-contactform-address-seller">Street Address</label>
                                            <input type="text" id="template-contactform-address-seller"
                                                   name="street_address"
                                                   class="sm-form-control required"/>
                                        </div>

                                        <div class="col_half col_last mb-2">
                                            <label for="template-contactform-city-seller">City</label>
                                            <input type="text" id="template-contactform-city-seller"
                                                   name="city"
                                                   class="sm-form-control required"/>
                                        </div>
                                        <div class="col_half mb-2">
                                            <label for="template-contactform-state-seller">State</label>
                                            <select id="template-contactform-state-seller" name="state"
                                                    class="sm-form-control">
                                                <option value="">State</option>
                                                <option value="AL">
                                                    Alabama
                                                </option>
                                                <option value="AK">
                                                    Alaska
                                                </option>
                                                <option value="AB">
                                                    Alberta
                                                </option>
                                                <option value="AS">
                                                    American Samoa
                                                </option>
                                                <option value="AZ">
                                                    Arizona
                                                </option>
                                                <option value="AR">
                                                    Arkansas
                                                </option>
                                                <option value="BC">
                                                    British Columbia
                                                </option>
                                                <option value="CA">
                                                    California
                                                </option>
                                                <option value="CO">
                                                    Colorado
                                                </option>
                                                <option value="CT">
                                                    Connecticut
                                                </option>
                                                <option value="DE">
                                                    Delaware
                                                </option>
                                                <option value="FM">
                                                    Fed. St. of Micronesia
                                                </option>
                                                <option value="FL">
                                                    Florida
                                                </option>
                                                <option value="GA">
                                                    Georgia
                                                </option>
                                                <option value="GU">
                                                    Guam
                                                </option>
                                                <option value="HI">
                                                    Hawaii
                                                </option>
                                                <option value="ID">
                                                    Idaho
                                                </option>
                                                <option value="IL">
                                                    Illinois
                                                </option>
                                                <option value="IN">
                                                    Indiana
                                                </option>
                                                <option value="IA">
                                                    Iowa
                                                </option>
                                                <option value="KS">
                                                    Kansas
                                                </option>
                                                <option value="KY">
                                                    Kentucky
                                                </option>
                                                <option value="LA">
                                                    Louisiana
                                                </option>
                                                <option value="ME">
                                                    Maine
                                                </option>
                                                <option value="MB">
                                                    Manitoba
                                                </option>
                                                <option value="MH">
                                                    Marshall Islands
                                                </option>
                                                <option value="MD">
                                                    Maryland
                                                </option>
                                                <option value="MA">
                                                    Massachusetts
                                                </option>
                                                <option value="MI">
                                                    Michigan
                                                </option>
                                                <option value="MN">
                                                    Minnesota
                                                </option>
                                                <option value="MS">
                                                    Mississippi
                                                </option>
                                                <option value="MO">
                                                    Missouri
                                                </option>
                                                <option value="MT">
                                                    Montana
                                                </option>
                                                <option value="NE">
                                                    Nebraska
                                                </option>
                                                <option value="NV">
                                                    Nevada
                                                </option>
                                                <option value="NB">
                                                    New Brunswick
                                                </option>
                                                <option value="NH">
                                                    New Hampshire
                                                </option>
                                                <option value="NJ">
                                                    New Jersey
                                                </option>
                                                <option value="NM">
                                                    New Mexico
                                                </option>
                                                <option value="NY">
                                                    New York
                                                </option>
                                                <option value="NL">
                                                    Newfoundland
                                                </option>
                                                <option value="NC">
                                                    North Carolina
                                                </option>
                                                <option value="ND">
                                                    North Dakota
                                                </option>
                                                <option value="MP">
                                                    Northern Mariana Islands
                                                </option>
                                                <option value="NT">
                                                    Northwest Territory
                                                </option>
                                                <option value="NS">
                                                    Nova Scotia
                                                </option>
                                                <option value="NU">
                                                    Nunavut
                                                </option>
                                                <option value="OH">
                                                    Ohio
                                                </option>
                                                <option value="OK">
                                                    Oklahoma
                                                </option>
                                                <option value="ON">
                                                    Ontario
                                                </option>
                                                <option value="OR">
                                                    Oregon
                                                </option>
                                                <option value="PA">
                                                    Pennsylvania
                                                </option>
                                                <option value="PE">
                                                    Prince Edward Island
                                                </option>
                                                <option value="PR">
                                                    Puerto Rico
                                                </option>
                                                <option value="QC">
                                                    Quebec
                                                </option>
                                                <option value="RI">
                                                    Rhode Island
                                                </option>
                                                <option value="SK">
                                                    Saskatchewan
                                                </option>
                                                <option value="SC">
                                                    South Carolina
                                                </option>
                                                <option value="SD">
                                                    South Dakota
                                                </option>
                                                <option value="TN">
                                                    Tennessee
                                                </option>
                                                <option value="TX">
                                                    Texas
                                                </option>
                                                <option value="UT">
                                                    Utah
                                                </option>
                                                <option value="VT">
                                                    Vermont
                                                </option>
                                                <option value="VI">
                                                    Virgin Islands
                                                </option>
                                                <option value="VA">
                                                    Virginia
                                                </option>
                                                <option value="WA">
                                                    Washington
                                                </option>
                                                <option value="DC">
                                                    Washington DC
                                                </option>
                                                <option value="WV">
                                                    West Virginia
                                                </option>
                                                <option value="WI">
                                                    Wisconsin
                                                </option>
                                                <option value="WY">
                                                    Wyoming
                                                </option>
                                                <option value="YT">
                                                    Yukon Territory
                                                </option>
                                            </select>
                                        </div>
                                        <div class="col_half col_last mb-2">
                                            <label for="template-contactform-zip-seller">Zip/Postal Code</label>
                                            <input type="text" id="template-contactform-zip-seller"
                                                   name="zip"
                                                   class="sm-form-control required"/>
                                        </div>
                                        <div class="col_half mb-1">
                                            <label for="template-contactform-is_home_listed-seller"> Is home
                                                listed?</label>
                                            <select id="template-contactform-is_home_listed-seller"
                                                    name="is_home_listed" class="sm-form-control">
                                                <option value="">Is home listed?</option>
                                            </select>
                                        </div>
                                        <div class="col_half col_last mb-2">
                                            <label for="template-contactform-asking_price-seller">Asking
                                                Price</label>
                                            <input type="number" id="template-contactform-asking_price-seller"
                                                   name="asking_price"
                                                   class="sm-form-control required" min="0"/>
                                        </div>
                                    </div>


                                    <div class="col_full mb-2 pt-2">
                                        <button class="button btn-block button-3d nomargin" type="submit"
                                                name="template-contactform-submit" id="template-contactform-seller"
                                                value="submit"> Get your ebook
                                        </button>
                                    </div>

                                </form>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

        </div>
    </section>

    <!-- Content
    ============================================= -->
    <section id="content">

        <div class="content-wrap nobottompadding">

            <div class="promo promo-light promo-full uppercase bottommargin-lg header-stick">
                <div class="container clearfix">
                    <h3 style="letter-spacing: 2px;" id="about_us_title">Little More Detail About Us</h3>
                    <span id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</span>
                </div>
            </div>

            <div class="section nobg notopmargin  pt-0 footer-stick mb-3">
                <div class="container clearfix">

                    <div class="row">
                        <div class="col-lg-6 mb-2">
                            <a class="video_section_thumbnail" id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8"
                               data-lightbox="iframe">
                                <img src="/static/xsite_template/images/video_thumbnail.jpg" alt="Youtube Video"
                                     class="image_fade"
                                     style="box-shadow: 0px 0px 25px 0px rgba(0,0,0,0.15); border-radius: 6px;">
                                <i class="fa fa-play"
                                   style="position: absolute; top: 50%; left: 50%; font-size: 60px; color: #FFF; margin-top: -45px; margin-left: -23px"></i>
                            </a>
                        </div>
                        <div class="col-lg-6 notopmargin ">
                            <div class="heading-block nobottomborder">
                                <h2 id="video_title">Video</h2>
                                <span class="ls1" id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</span>

                            </div>

                        </div>
                    </div>

                </div>
            </div>
            <div class="section parallax dark"
                 style="background-image: url('/static/xsite_template/all_templates/xsite_template_one/images/slider/3.jpg'); padding: 120px 0;"
                 data-bottom-top="background-position:0px 0px;" data-top-bottom="background-position:0px -600px;">

                <div class="fslider testimonial testimonial-full" data-arrows="false" style="z-index: 2;">
                    <div id="testimonial_class" class="testimonial_class flexslider">
                        <div class="slider-wrap">
                            <div class="slide">

                                <div class="testi-content">
                                    <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_1_person_name">Person 1</span>
                                        <span id="testi_1_company_name">Argon 1</span>
                                    </div>
                                </div>
                            </div>
                                <div class="slide">

                                    <div class="testi-content">
                                        <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_2_person_name">Person 2</span>
                                            <span id="testi_2_company_name">Argon 2</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="slide">

                                    <div class="testi-content">
                                        <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_3_person_name">Person 3</span>
                                            <span id="testi_3_company_name">Argon 3</span>
                                        </div>
                                    </div>
                                </div>
                        </div>
                    </div>
                </div>

                <div class="video-wrap" style="z-index: 1;">
                    <div class="video-overlay" style="background: rgba(55,80,31,0.9);"></div>
                </div>

            </div>


            <div class="promo promo-light promo-full uppercase   header-stick">
                <div class="container clearfix">
                    <h3 id="other_details_title" style="letter-spacing: 2px;">More To Know Us</h3>
                    <span id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?</span>
                </div>
            </div>

        </div>

        <a href="#"
           class="button button-3d nobottomborder button-full center tright t300 font-primary bg_green enquire_btn"
           style="font-size: 26px;">
            <div class="container clearfix">
                <span id="call_to_action_text">Nothing</span> <strong>Enquire Here</strong> <i
                    class="fa fa-angle-right" style="top:3px;"></i>
            </div>
        </a>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="dark">

        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="p-0">

            <div class="container clearfix">

                <div class="text-center">
                    &copy; 2020 <a class="footer_copyright" target="_blank" href="https://prospectx.com/">Prospectx</a>
                    All Rights Reserved.
                </div>


            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->

</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="icon-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>

</body>"""

    Violet_head = """<head>      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">     <meta http-equiv="X-UA-Compatible" content="IE=edge"/>     <meta http-equiv="X-UA-Compatible" content="ie=edge">     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <meta name="robots" content="noarchive">     <title>Xsite</title>          <!-- bootstrap -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_two/assets/css/bootstrap.min.css">     <!-- icofont -->     <link rel="stylesheet"           href="/static/xsite_template/all_templates/xsite_template_two/assets/css/fontawesome.5.7.2.css">     <!-- flaticon -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_two/assets/css/flaticon.css">     <!-- animate.css -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_two/assets/css/animate.css">     <!-- Owl Carousel -->     <link rel="stylesheet"           href="/static/xsite_template/all_templates/xsite_template_two/assets/css/owl.carousel.min.css">     <!-- magnific popup -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_two/assets/css/magnific-popup.css">     <!-- stylesheet -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_two/assets/css/style.css">     <!-- responsive -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_two/assets/css/responsive.css">      <link href="/static/assets/custom_css/toastr.new.min.css" rel="stylesheet" type="text/css">
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css"> </head>"""
    Violet_body = """<body>

<nav class="navbar navbar-area navbar-expand-lg nav-absolute white nav-style-01">
    <div class="container nav-container">
        <div class="responsive-mobile-menu">
            <div class="logo-wrapper">
                <a href="#" class="logo">
                    <img id="logo" src="/media/xsite_images/website_logos/prospectx-logo.png" alt="logo">
                </a>
            </div>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#appside_main_menu"
                    aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>
        <div class="collapse navbar-collapse" id="appside_main_menu">
            <ul class="navbar-nav">
                <li class="current-menu-item">
                    <a href="#">Home</a>
                </li>
                <li><a href="#about">About</a></li>
                <li><a href="#more_details">Details</a></li>
                <li><a href="#testimonial">Testimonial</a></li>
            </ul>
        </div>
        <div class="nav-right-content">
            <ul>
                <li class="button-wrapper">
                    <a id="phone" href="tel:03214568751" class="boxed-btn btn-rounded">Call Us 03334455667</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!-- header area start  -->
<header class="header-area header-bg-5 style-five" id="home">
    <div class="container">
        <div class="row">
            <div class="col-lg-7">
                <div class="header-inner">
                    <h1 id="banner_title1" class="title wow fadeInDown">Find Your Dream Home Here! Beautiful Homes At
                        Ugly Home Prices.
                    </h1>
                </div>
            </div>
            <div class="col-lg-5">
                <div class="header-form-area">
                    <div class="header-form-inner wow fadeInUp" id="form">
                        <h4 id="banner_title" class="title">Find Your Dream Home Here! Beautiful Homes At Ugly Home
                            Prices. </h4>
                            <form id="buyer_form" class="get-quote-form" name="template-contactform"
                                  method="post">
                                <div class="form-group">
                                    <input type="text"
                                           name="fullname"
                                           id="template-contactform-name-buyer"
                                           class="form-control" placeholder="Enter Your Name.."/>
                                </div>

                                <div class="form-group">
                                    <input type="email"
                                           name="email"
                                           id="template-contactform-email-buyer"
                                           class="form-control" placeholder="Enter Your Email.."/>
                                </div>

                                <div class="clear"></div>

                                <div class="form-group">
                                    <input type="text" id="template-contactform-phone-buyer"
                                           name="phone"
                                           class="form-control" placeholder="Enter Phone.."/>
                                </div>
                                <div class="form-group">
                                    <select id="template-contactform-service-buyer"
                                            name="what_are_you_looking_for"
                                            class="form-control">
                                        <option value="">What are you looking for?</option>
                                    </select>

                                </div>
                                <input type="hidden" name="audience" value="Buyer">
                                <button class="submit-btn"
                                        type="submit"
                                        name="template-contactform-submit"
                                        id="template-contactform-submit-buyer"
                                        value="submit"> Get Your E-book

                                </button>
                            </form>

                        <form id="seller_form" class="get-quote-form" name="template-contactform"
                              method="post">
                            <input type="hidden" name="audience" value="Seller">
                            <div class="form-group">
                                <input type="text" id="template-contactform-name-seller"
                                       name="fullname"
                                       class="form-control" placeholder="Enter Your Name.."/>
                            </div>
                            <div class="form-group">
                                <input type="text" id="template-contactform-phone-seller"
                                       name="phone"
                                       class="form-control" placeholder="Enter Phone.."/>
                            </div>
                            <div class="form-group">
                                <input type="email" id="template-contactform-email-seller"
                                       name="email"
                                       class="form-control" placeholder="Enter Your Email.."/>
                            </div>

                            <div class="mb-3">

                                <div class="form-check">
                                    <label class="form-check-label">

                                        <input name="immediate_assistance"
                                               id="immediate_assistance" type="checkbox"
                                               class="form-check-input"
                                               onclick="javascript:ShowFields()">
                                        I
                                        would like
                                        immediate assistance
                                    </label>
                                </div>
                            </div>

                            <div id="immediate_assistance_fields" style="display: none">
                                <div class="form-group">
                                    <input type="text"
                                           id="template-contactform-address-seller"
                                           name="street_address"
                                           class="form-control" placeholder="Enter Your Street Address.."/>
                                </div>

                                <div class="form-group">
                                    <input type="text" id="template-contactform-city-seller"
                                           name="city"
                                           class="form-control" placeholder="Enter Your City.."/>
                                </div>
                                <div class="form-group">
                                    <select id="template-contactform-state-seller"
                                            name="state"
                                            class="form-control">
                                        <option value="">State</option>
                                        <option value="AL">
                                            Alabama
                                        </option>
                                        <option value="AK">
                                            Alaska
                                        </option>
                                        <option value="AB">
                                            Alberta
                                        </option>
                                        <option value="AS">
                                            American Samoa
                                        </option>
                                        <option value="AZ">
                                            Arizona
                                        </option>
                                        <option value="AR">
                                            Arkansas
                                        </option>
                                        <option value="BC">
                                            British Columbia
                                        </option>
                                        <option value="CA">
                                            California
                                        </option>
                                        <option value="CO">
                                            Colorado
                                        </option>
                                        <option value="CT">
                                            Connecticut
                                        </option>
                                        <option value="DE">
                                            Delaware
                                        </option>
                                        <option value="FM">
                                            Fed. St. of Micronesia
                                        </option>
                                        <option value="FL">
                                            Florida
                                        </option>
                                        <option value="GA">
                                            Georgia
                                        </option>
                                        <option value="GU">
                                            Guam
                                        </option>
                                        <option value="HI">
                                            Hawaii
                                        </option>
                                        <option value="ID">
                                            Idaho
                                        </option>
                                        <option value="IL">
                                            Illinois
                                        </option>
                                        <option value="IN">
                                            Indiana
                                        </option>
                                        <option value="IA">
                                            Iowa
                                        </option>
                                        <option value="KS">
                                            Kansas
                                        </option>
                                        <option value="KY">
                                            Kentucky
                                        </option>
                                        <option value="LA">
                                            Louisiana
                                        </option>
                                        <option value="ME">
                                            Maine
                                        </option>
                                        <option value="MB">
                                            Manitoba
                                        </option>
                                        <option value="MH">
                                            Marshall Islands
                                        </option>
                                        <option value="MD">
                                            Maryland
                                        </option>
                                        <option value="MA">
                                            Massachusetts
                                        </option>
                                        <option value="MI">
                                            Michigan
                                        </option>
                                        <option value="MN">
                                            Minnesota
                                        </option>
                                        <option value="MS">
                                            Mississippi
                                        </option>
                                        <option value="MO">
                                            Missouri
                                        </option>
                                        <option value="MT">
                                            Montana
                                        </option>
                                        <option value="NE">
                                            Nebraska
                                        </option>
                                        <option value="NV">
                                            Nevada
                                        </option>
                                        <option value="NB">
                                            New Brunswick
                                        </option>
                                        <option value="NH">
                                            New Hampshire
                                        </option>
                                        <option value="NJ">
                                            New Jersey
                                        </option>
                                        <option value="NM">
                                            New Mexico
                                        </option>
                                        <option value="NY">
                                            New York
                                        </option>
                                        <option value="NL">
                                            Newfoundland
                                        </option>
                                        <option value="NC">
                                            North Carolina
                                        </option>
                                        <option value="ND">
                                            North Dakota
                                        </option>
                                        <option value="MP">
                                            Northern Mariana Islands
                                        </option>
                                        <option value="NT">
                                            Northwest Territory
                                        </option>
                                        <option value="NS">
                                            Nova Scotia
                                        </option>
                                        <option value="NU">
                                            Nunavut
                                        </option>
                                        <option value="OH">
                                            Ohio
                                        </option>
                                        <option value="OK">
                                            Oklahoma
                                        </option>
                                        <option value="ON">
                                            Ontario
                                        </option>
                                        <option value="OR">
                                            Oregon
                                        </option>
                                        <option value="PA">
                                            Pennsylvania
                                        </option>
                                        <option value="PE">
                                            Prince Edward Island
                                        </option>
                                        <option value="PR">
                                            Puerto Rico
                                        </option>
                                        <option value="QC">
                                            Quebec
                                        </option>
                                        <option value="RI">
                                            Rhode Island
                                        </option>
                                        <option value="SK">
                                            Saskatchewan
                                        </option>
                                        <option value="SC">
                                            South Carolina
                                        </option>
                                        <option value="SD">
                                            South Dakota
                                        </option>
                                        <option value="TN">
                                            Tennessee
                                        </option>
                                        <option value="TX">
                                            Texas
                                        </option>
                                        <option value="UT">
                                            Utah
                                        </option>
                                        <option value="VT">
                                            Vermont
                                        </option>
                                        <option value="VI">
                                            Virgin Islands
                                        </option>
                                        <option value="VA">
                                            Virginia
                                        </option>
                                        <option value="WA">
                                            Washington
                                        </option>
                                        <option value="DC">
                                            Washington DC
                                        </option>
                                        <option value="WV">
                                                West Virginia
                                        </option>
                                        <option value="WI">
                                            Wisconsin
                                        </option>
                                        <option value="WY">
                                            Wyoming
                                        </option>
                                        <option value="YT">
                                            Yukon Territory
                                        </option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <input type="text" id="template-contactform-zip-seller"
                                           name="zip"
                                           class="form-control" placeholder="Enter Your Zip.."/>

                                </div>
                                <div class="form-group">
                                    <select id="template-contactform-is_home_listed-seller"
                                            name="is_home_listed" class="form-control">
                                        <option value="">Is home listed?</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <input type="number"
                                           id="template-contactform-asking_price-seller"
                                           name="asking_price"
                                           class="form-control" placeholder="Enter Your Asking Price.."
                                           min="0"/>
                                </div>
                            </div>
                            <button class="submit-btn"
                                    type="submit"
                                    name="template-contactform-submit"
                                    id="template-contactform-seller"
                                    value="submit"> Get Your E-book
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</header>
<!-- header area end  -->

<!-- about us area start -->

<section class="about-us-area style-two" id="about">
    <div class="container">
        <div class="row">
            <div class="col-lg-6">
                <div class="section-title left-aligned">
                    <!-- section title -->
                    <span class="subtitle">About</span>
                    <h3 id="about_us_title" class="title extra">Little More Detail About Us</h3>
                </div><!-- //. section title -->
            </div>
            <div class="col-lg-6">
                <div class="feature-area mt-5">
                    <p id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt? </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- about us area end -->
<!-- video area start -->
<section class="video-area  about-us-area style-two">
    <div class="container">
        <div class="row">
            <div class="col-lg-6">
                <div class="img-with-video">
                    <div class="img-wrap">
                        <img src="/static/xsite_template/all_templates/xsite_template_two/assets/img/video-image.jpg"
                             alt="">
                        <div class="hover">
                            <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8"
                               class="video-play-btn mfp-iframe"><i class="fa fa-play"></i></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="right-content-area mt-0">
                    <h3 id="video_title" class="title">Video</h3>
                    <p id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</p>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- video area end -->


<!-- why choose area start -->
<section class="why-choose-area why-choose-us-bg" id="more_details">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-12">
                <div class="section-title white mb-1">
                    <!-- section title -->
                    <span class="subtitle">More details</span>
                    <h3 id="other_details_title" class="title extra">More To Know Us</h3>
                    <p id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
                    </p>
                </div><!-- //. section title -->
            </div>
        </div>
    </div>
</section>
<!-- why choose area end -->

<!-- testimonial area start -->
<section class="testimonial-area pt-4 pb-4" id="testimonial">
    <div class="shape-1"><img
            src="/static/xsite_template/all_templates/xsite_template_two/assets/img/shape/08.png" alt="">
    </div>
    <div class="shape-2"><img
            src="/static/xsite_template/all_templates/xsite_template_two/assets/img/shape/09.png" alt="">
    </div>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="section-title ">
                    <!-- section title -->
                    <span class="subtitle">Testimonial</span>
                    <h3 class="title extra">What People Say</h3>
                </div><!-- //. section title -->
            </div>
        </div>
        <div class="row">
            <div class="col-lg-12">
                <div class="testimonial-carousel" id="testimonials">

                    <div class="single-testimonial-item">
                        <!-- single testimonial item -->
                        <img src="/static/xsite_template/all_templates/xsite_template_two/assets/img/testimonial/001.png"
                             alt="">
                        <div class="hover">
                            <!-- hover -->
                            <div class="hover-inner">
                                <div class="icon"><i class="fa fa-quote-left"></i></div>
                                <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                <div class="author-meta">
                                    <h4 id="testi_1_person_name" class="name">Person 1</h4>
                                    <span id="testi_1_company_name" class="post">Argon Tech</span>
                                </div>
                            </div>
                        </div><!-- //. hover -->
                    </div><!-- //. single testimonial item -->
                    <div class="single-testimonial-item">
                        <!-- single testimonial item -->
                        <img src="/static/xsite_template/all_templates/xsite_template_two/assets/img/testimonial/002.png"
                             alt="">
                        <div class="hover">
                            <!-- hover -->
                            <div class="hover-inner">
                                <div class="icon"><i class="fa fa-quote-left"></i></div>
                                <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                <div class="author-meta">
                                    <h4 id="testi_2_person_name" class="name">Person 2</h4>
                                    <span id="testi_2_company_name" class="post">Argon Tech1</span>
                                </div>
                            </div>
                        </div><!-- //. hover -->
                    </div><!-- //. single testimonial item -->
                    <div class="single-testimonial-item">
                        <!-- single testimonial item -->
                        <img src="/static/xsite_template/all_templates/xsite_template_two/assets/img/testimonial/002.png"
                             alt="">
                        <div class="hover">
                            <!-- hover -->
                            <div class="hover-inner">
                                <div class="icon"><i class="fa fa-quote-left"></i></div>
                                <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                <div class="author-meta">
                                    <h4 id="testi_3_person_name" class="name">Person 3</h4>
                                    <span id="testi_3_company_name" class="post">Argon Tech2</span>
                                </div>
                            </div>
                        </div><!-- //. hover -->
                    </div><!-- //. single testimonial item -->
                </div>
            </div>
        </div>
    </div>
</section>
<!-- testimonial area end -->

<!-- footer area start -->
<footer class="footer-area">

    <div class="copyright-area">
        <!-- copyright area -->
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <div class="copyright-inner">
                        <!-- copyright inner wrapper -->
                        <div class="left-content-area">
                            <!-- left content area -->
                            &copy; 2020 <a target="_blank" href="https://prospectx.com/">Prospectx</a> All Rights
                            Reserved.
                        </div><!-- //. left content aera -->
                        <div class="right-content-area">
                            <!-- right content area -->
                            Designed by <strong><a target="_blank" href="https://prospectx.com/">Prospectx</a>
                        </strong>
                        </div><!-- //. right content area -->
                    </div><!-- //.copyright inner wrapper -->
                </div>
            </div>
        </div>
    </div><!-- //. copyright area -->
</footer>
<!-- footer area end -->

<!-- back to top area start -->
<div class="back-to-top">
    <i class="fa fa-angle-up"></i>
</div>
<!-- back to top area end -->

<!-- jquery -->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/jquery.js"></script>
<!-- popper -->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/popper.min.js"></script>
<!-- bootstrap -->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/bootstrap.min.js"></script>
<!-- owl carousel -->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/owl.carousel.min.js"></script>
<!-- magnific popup -->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/jquery.magnific-popup.js"></script>
<!-- contact js-->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/contact.js"></script>
<!-- wow js-->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/wow.min.js"></script>
<!-- way points js-->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/waypoints.min.js"></script>
<!-- counterup js-->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/jquery.counterup.min.js"></script>
<!-- main -->
<script src="/static/xsite_template/all_templates/xsite_template_two/assets/js/main.js"></script>

<script src="/static/assets/custom_js/toastr.min.js"></script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

 <script>
        $(document).ready(function () {
            $('#template-contactform-phone-buyer').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-phone-seller').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-zip-seller').focus(function () {
                var mask = "99999";
                $(this).inputmask(mask, {"placeholder": ""});
            });
        });
 </script>

</body>"""

    XBrownStone_head = """<head>      <meta http-equiv="content-type" content="text/html; charset=utf-8" /> 	<meta name="author" content="SemiColonWeb" />          <title>Xsite</title>  	<!-- Stylesheets 	============================================= --> 	<link href="http://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,900" rel="stylesheet" 		type="text/css" /> 	<link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css" /> 	<link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css" />  	<link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css" /> 	<link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css" /> 	<link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css" /> 	<link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css" />  	<!-- Bootstrap Switch CSS --> 	<link rel="stylesheet" href="/static/xsite_template/css/components/bs-switches.css" type="text/css" />  	<link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css" /> 	<meta name='viewport' content='initial-scale=1, viewport-fit=cover'>  	<!-- Seo Demo Specific Stylesheet --> 	<link rel="stylesheet" href="/static/xsite_template/css/colors.php?color=FE9603" type="text/css" /> <!-- Theme Color --> 	<link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_three/css/fonts.css" type="text/css" /> 	<link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_three/template_three.css" type="text/css" /> 
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">	<!-- / --> </head>"""
    XBrownStone_body = """<body class="stretched">

	<!-- Document Wrapper
	============================================= -->
	<div id="wrapper" class="clearfix">

        <!-- Top Bar
    ============================================= -->
    <div id="top-bar" class="transparent-topbar">

        <div class="container clearfix">


            <div class="col_half fright dark col_last clearfix nobottommargin">

                <!-- Top Social
                ============================================= -->
                <div id="top-social">
                    <ul>
                        <li><a href="#" class="si-facebook" target="_blank"><span class="ts-icon"><i
                                class="fab fa-facebook-f"></i></span><span class="ts-text">Facebook</span></a>
                        </li>
                        <li><a href="#" class="si-twitter" target="_blank"><span class="ts-icon"><i
                                class="fab fa-twitter"></i></span><span class="ts-text">Twitter</span></a>
                        </li>
                        <li><a href="#" class="si-youtube" target="_blank"><span class="ts-icon"><i
                                class="fab fa-youtube"></i></span><span class="ts-text">Youtube</span></a>
                        </li>
                        <li><a href="#" class="si-instagram" target="_blank"><span class="ts-icon"><i
                                class="fab fa-instagram"></i></span><span
                                class="ts-text">Instagram</span></a></li>
                        <li><a href="tel:+10.11.85412542" class="si-call"><span class="ts-icon"><i
                                class="fa fa-phone fa-flip-horizontal"></i></span><span
                                class="ts-text" id="phone">03334455667</span></a></li>
                        <li><a href="mailto:info@xsite.com" class="si-email3"><span class="ts-icon"><i
                                class="fa fa-envelope"></i></span><span
                                class="ts-text" id="email">support@gmail.com</span></a></li>
                    </ul>
                </div><!-- #top-social end -->

            </div>

        </div>

    </div><!-- #top-bar end -->

    <!-- Header
    ============================================= -->
    <header id="header" class="transparent-header floating-header clearfix">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo" data-dark-logo="images/logo-dark.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Xsite Logo"></a>
                    <a href="#" class="retina-logo" data-dark-logo="images/logo-dark@2x.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Xsite Logo"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigationlogo.png
                ============================================= -->
                <nav id="primary-menu" class="with-arrows">

                    <ul onclick="active_class_function(event)">
                        <li class="current"><a href="#">
                            <div>Home</div>
                        </a></li>
                        <li><a href="#about">
                            <div>About</div>
                        </a></li>
                        <li><a href="#get_ebook">
                            <div>Details</div>
                        </a></li>
                        <li><a href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                    </ul>

                    <!-- Menu Buttons
                    ============================================= -->
                    <a href="#get_ebook"
                       class="button button-rounded fright leftmargin-sm banner_button_text">Get Your Ebook</a>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element slider-parallax full-screen clearfix"
             style="background: #FFF url('/static/xsite_template/all_templates/xsite_template_three/images/hero/hero-3.jpg') center center no-repeat; background-size: cover;">

        <div class="vertical-middle">
            <div class="container topmargin-sm">
                <div class="row">
                    <div class="col-lg-6 col-md-8">
                        <div class="slider-title">
                            <h2 id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home
                            Prices. </h2>
                            <a href="#get_ebook"
                               class="button button-rounded button-large nott ls0 banner_button_text">Get Your Ebook</a>
                        </div>
                    </div>
                </div>
            </div>

        </div>


    </section><!-- #slider end -->

    <!-- Content
    ============================================= -->
    <section id="content">

        <div class="content-wrap pt-0 pb-0">

            <!-- Features
            ============================================= -->
            <div class="section nobg mt-4 mb-0 pb-0" id="about" style="padding: 80px 0;">
                <div class="container">
                    <div class="heading-block nobottomborder center divcenter mb-0 clearfix">
                        <div class="badge badge-pill badge-default">About</div>
                        <h3 id="about_us_title" class="nott ls0 mb-3">Little More Detail About Us</h3>
                        <p id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?
                        </p>
                    </div>

                </div>
            </div>

            <!--
            ============================================= -->
            <div class="section m-0" id="get_ebook"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/4.png') no-repeat center top; background-size: cover; padding: 100px 0 0;">
                <div class="container">
                    <div class="row justify-content-between">
                        <div class="col-lg-8  col-md-8 ">
                            <div class="heading-block nobottomborder bottommargin-sm">
                                <div class="badge badge-pill badge-default">More Details</div>
                                <h3 id="other_details_title" class="nott ls0">More To Know Us</h3>
                            </div>
                            <p id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt? </p>
                        </div>

                        <div class="col-lg-4 col-md-4">
                            <div id="section-pricing" class="page-section nopadding nomargin">

                                <div id="pricing-switch"
                                     class="pricing row align-items-end topmargin-sm bottommargin-lg clearfix">
                                    <div class="card shadow-sm">
                                        <div class="card-body">
                                            <h4 class="mb-3">We give FAIR cash offers for your home! Fill out the form on to get an offer!</h4>
                                            <div class="form-widget">
                                                <div class="form-result"></div>
                                                    <form id="buyer_form" class="nobottommargin" name="template-contactform"
                                                          method="post">
                                                        <div class="form-process"></div>

                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-name-buyer">Name
                                                                <small>*</small></label>
                                                            <input type="text"
                                                                   name="fullname"
                                                                   id="template-contactform-name-buyer"
                                                                   class="form-control input-sm required"/>
                                                        </div>

                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-email-buyer">Email
                                                                <small>*</small></label>
                                                            <input type="email"
                                                                   name="email"
                                                                   id="template-contactform-email-buyer"
                                                                   class="form-control input-sm required"/>
                                                        </div>

                                                        <div class="clear"></div>

                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-phone-buyer">Phone<small>*</small></label>
                                                            <input type="text" id="template-contactform-phone-buyer"
                                                                   name="phone"
                                                                   class="form-control input-sm required"/>
                                                        </div>
                                                        <div class="col_full mb-4">
                                                            <label for="template-contactform-service-buyer">What are you
                                                                looking
                                                                for?</label>
                                                            <select id="template-contactform-service-buyer"
                                                                    name="what_are_you_looking_for"
                                                                    class="sm-form-control">
                                                                <option value="">What are you looking for?</option>
                                                            </select>

                                                        </div>
                                                        <input type="hidden" name="audience" value="Buyer">
                                                        <div class="col_full nobottommargin">
                                                            <button class="button button-rounded btn-block nott ls0 m-0"
                                                                    type="submit"
                                                                    name="template-contactform-submit"
                                                                    id="template-contactform-submit-buyer"
                                                                    value="submit"> GET Your Ebook

                                                            </button>
                                                        </div>
                                                    </form>
                                                    <form id="seller_form" class="nobottommargin" name="template-contactform"
                                                          method="post">
                                                        <input type="hidden" name="audience" value="Seller">
                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-name-seller">Name
                                                                <small>*</small></label>
                                                            <input type="text" id="template-contactform-name-seller"
                                                                   name="fullname"
                                                                   class="form-control input-sm required"/>
                                                        </div>
                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-phone-seller">Phone<small>*</small></label>
                                                            <input type="text" id="template-contactform-phone-seller"
                                                                   name="phone"
                                                                   class="form-control input-sm required"/>
                                                        </div>
                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-email-seller">Email
                                                                <small>*</small></label>
                                                            <input type="email" id="template-contactform-email-seller"
                                                                   name="email"
                                                                   class="form-control input-sm required"/>
                                                        </div>

                                                        <div class="col_full mb-3 pt-3">

                                                            <div class="form-check">
                                                                <label class="form-check-label">

                                                                    <input name="immediate_assistance"
                                                                           id="immediate_assistance" type="checkbox"
                                                                           class="form-check-input"
                                                                           onclick="javascript:ShowFields()">
                                                                    I
                                                                    would like
                                                                    immediate assistance
                                                                </label>
                                                            </div>
                                                        </div>

                                                        <div id="immediate_assistance_fields" style="display: none">
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-address-seller">Street
                                                                    Address</label>
                                                                <input type="text"
                                                                       id="template-contactform-address-seller"
                                                                       name="street_address"
                                                                       class="form-control input-sm required"/>
                                                            </div>

                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-city-seller">City</label>
                                                                <input type="text" id="template-contactform-city-seller"
                                                                       name="city"
                                                                       class="form-control input-sm required"/>
                                                            </div>
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-state-seller">State</label>
                                                                <select id="template-contactform-state-seller"
                                                                        name="state"
                                                                        class="sm-form-control">
                                                                    <option value="">State</option>
                                                                    <option value="AL">
                                                                        Alabama
                                                                    </option>
                                                                    <option value="AK">
                                                                        Alaska
                                                                    </option>
                                                                    <option value="AB">
                                                                        Alberta
                                                                    </option>
                                                                    <option value="AS">
                                                                        American Samoa
                                                                    </option>
                                                                    <option value="AZ">
                                                                        Arizona
                                                                    </option>
                                                                    <option value="AR">
                                                                        Arkansas
                                                                    </option>
                                                                    <option value="BC">
                                                                        British Columbia
                                                                    </option>
                                                                    <option value="CA">
                                                                        California
                                                                    </option>
                                                                    <option value="CO">
                                                                        Colorado
                                                                    </option>
                                                                    <option value="CT">
                                                                        Connecticut
                                                                    </option>
                                                                    <option value="DE">
                                                                        Delaware
                                                                    </option>
                                                                    <option value="FM">
                                                                        Fed. St. of Micronesia
                                                                    </option>
                                                                    <option value="FL">
                                                                        Florida
                                                                    </option>
                                                                    <option value="GA">
                                                                        Georgia
                                                                    </option>
                                                                    <option value="GU">
                                                                        Guam
                                                                    </option>
                                                                    <option value="HI">
                                                                        Hawaii
                                                                    </option>
                                                                    <option value="ID">
                                                                        Idaho
                                                                    </option>
                                                                    <option value="IL">
                                                                        Illinois
                                                                    </option>
                                                                    <option value="IN">
                                                                        Indiana
                                                                    </option>
                                                                    <option value="IA">
                                                                        Iowa
                                                                    </option>
                                                                    <option value="KS">
                                                                        Kansas
                                                                    </option>
                                                                    <option value="KY">
                                                                        Kentucky
                                                                    </option>
                                                                    <option value="LA">
                                                                        Louisiana
                                                                    </option>
                                                                    <option value="ME">
                                                                        Maine
                                                                    </option>
                                                                    <option value="MB">
                                                                        Manitoba
                                                                    </option>
                                                                    <option value="MH">
                                                                        Marshall Islands
                                                                    </option>
                                                                    <option value="MD">
                                                                        Maryland
                                                                    </option>
                                                                    <option value="MA">
                                                                        Massachusetts
                                                                    </option>
                                                                    <option value="MI">
                                                                        Michigan
                                                                    </option>
                                                                    <option value="MN">
                                                                        Minnesota
                                                                    </option>
                                                                    <option value="MS">
                                                                        Mississippi
                                                                    </option>
                                                                    <option value="MO">
                                                                        Missouri
                                                                    </option>
                                                                    <option value="MT">
                                                                        Montana
                                                                    </option>
                                                                    <option value="NE">
                                                                        Nebraska
                                                                    </option>
                                                                    <option value="NV">
                                                                        Nevada
                                                                    </option>
                                                                    <option value="NB">
                                                                        New Brunswick
                                                                    </option>
                                                                    <option value="NH">
                                                                        New Hampshire
                                                                    </option>
                                                                    <option value="NJ">
                                                                        New Jersey
                                                                    </option>
                                                                    <option value="NM">
                                                                        New Mexico
                                                                    </option>
                                                                    <option value="NY">
                                                                        New York
                                                                    </option>
                                                                    <option value="NL">
                                                                        Newfoundland
                                                                    </option>
                                                                    <option value="NC">
                                                                        North Carolina
                                                                    </option>
                                                                    <option value="ND">
                                                                        North Dakota
                                                                    </option>
                                                                    <option value="MP">
                                                                        Northern Mariana Islands
                                                                    </option>
                                                                    <option value="NT">
                                                                        Northwest Territory
                                                                    </option>
                                                                    <option value="NS">
                                                                        Nova Scotia
                                                                    </option>
                                                                    <option value="NU">
                                                                        Nunavut
                                                                    </option>
                                                                    <option value="OH">
                                                                        Ohio
                                                                    </option>
                                                                    <option value="OK">
                                                                        Oklahoma
                                                                    </option>
                                                                    <option value="ON">
                                                                        Ontario
                                                                    </option>
                                                                    <option value="OR">
                                                                        Oregon
                                                                    </option>
                                                                    <option value="PA">
                                                                        Pennsylvania
                                                                    </option>
                                                                    <option value="PE">
                                                                        Prince Edward Island
                                                                    </option>
                                                                    <option value="PR">
                                                                        Puerto Rico
                                                                    </option>
                                                                    <option value="QC">
                                                                        Quebec
                                                                    </option>
                                                                    <option value="RI">
                                                                        Rhode Island
                                                                    </option>
                                                                    <option value="SK">
                                                                        Saskatchewan
                                                                    </option>
                                                                    <option value="SC">
                                                                        South Carolina
                                                                    </option>
                                                                    <option value="SD">
                                                                        South Dakota
                                                                    </option>
                                                                    <option value="TN">
                                                                        Tennessee
                                                                    </option>
                                                                    <option value="TX">
                                                                        Texas
                                                                    </option>
                                                                    <option value="UT">
                                                                        Utah
                                                                    </option>
                                                                    <option value="VT">
                                                                        Vermont
                                                                    </option>
                                                                    <option value="VI">
                                                                        Virgin Islands
                                                                    </option>
                                                                    <option value="VA">
                                                                        Virginia
                                                                    </option>
                                                                    <option value="WA">
                                                                        Washington
                                                                    </option>
                                                                    <option value="DC">
                                                                        Washington DC
                                                                    </option>
                                                                    <option value="WV">
                                                                            West Virginia
                                                                    </option>
                                                                    <option value="WI">
                                                                        Wisconsin
                                                                    </option>
                                                                    <option value="WY">
                                                                        Wyoming
                                                                    </option>
                                                                    <option value="YT">
                                                                        Yukon Territory
                                                                    </option>
                                                                </select>
                                                            </div>
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-zip-seller">Zip/Postal
                                                                    Code</label>
                                                                <input type="text" id="template-contactform-zip-seller"
                                                                       name="zip"
                                                                       class="form-control input-sm required"/>

                                                            </div>
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-is_home_listed-seller">
                                                                    Is
                                                                    home listed?</label>
                                                                <select id="template-contactform-is_home_listed-seller"
                                                                        name="is_home_listed" class="sm-form-control">
                                                                    <option value="">Is home listed?</option>
                                                                </select>
                                                            </div>
                                                            <div class="col_full mb-4">
                                                                <label for="template-contactform-asking_price-seller">Asking
                                                                    Price</label>
                                                                <input type="number"
                                                                       id="template-contactform-asking_price-seller"
                                                                       name="asking_price"
                                                                       class="form-control input-sm required" min="0"/>
                                                            </div>
                                                        </div>


                                                        <div class="col_full nobottommargin">
                                                            <button class="button button-rounded btn-block nott ls0 m-0"
                                                                    type="submit"
                                                                    name="template-contactform-submit"
                                                                    id="template-contactform-seller"
                                                                    value="submit"> GET youur ebook
                                                            </button>
                                                        </div>
                                                    </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>
            </div>

            <!-- Form Section
            ============================================= -->
            <div class="section m-0"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/1.jpg') no-repeat center center; background-size: cover; padding: 100px 0;">
                <div class="container">
                    <div class="row justify-content-between align-items-center">

                        <div class="col-md-6">
                            <div class="heading-block nobottomborder bottommargin-sm">
                                <h3 id="video_title" class="nott ls0">Title</h3>
                            </div>
                            <p id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt? </p>

                        </div>


                        <div class="col-md-4 mt-5 mt-md-0 center">
                            <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe"
                               class="play-icon shadow"><i class="fa fa-play"></i></a>
                        </div>

                    </div>

                </div>
            </div>


            <!-- Testimonials
            ============================================= -->
            <div class="section mt-0" id="testimonails"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/3.jpg') no-repeat top center; background-size: cover; padding: 80px 0 70px;">
                <div class="container">
                    <div class="heading-block nobottomborder center">
                        <div class="badge badge-pill badge-default">Testimonials</div>
                        <h3 class="nott ls0">What Clients Says</h3>
                    </div>

                    <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget clearfix"
                         data-margin="0" data-pagi="true" data-loop="true" data-center="true" data-autoplay="5000"
                         data-items-sm="1" data-items-md="2" data-items-xl="3">

                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-image">
                                    <a href="#"><img
                                            src="/static/xsite_template/all_templates/xsite_template_three/images/avatar.png"
                                            alt="Customer Testimonails"></a>
                                </div>
                                <div class="testi-content">
                                    <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_1_person_name">Person 1</span>
                                        <span id="testi_1_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="oc-item">
                                <div class="testimonial">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_three/images/avatar.png"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_2_person_name">Person 1</span>
                                            <span id="testi_2_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="oc-item">
                                <div class="testimonial">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_three/images/avatar.png"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_3_person_name">Person 1</span>
                                            <span id="testi_3_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                    </div>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="noborder bg-white">
        <!-- Copyrights
        ============================================= -->
        <div id="copyrights"
             style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/hero/footer.svg') no-repeat top center; background-size: cover; padding-top: 70px;">
            <div class="container clearfix">
                <div class="col_half">
                    &copy; 2020 <a target="_blank" href="https://prospectx.com/">Prospectx</a> All Rights Reserved.
                </div>
            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->


</div><!-- #wrapper end -->

	<!-- Go To Top
	============================================= -->
	<div id="gotoTop" class="fa fa-angle-up"></div>

	<!-- External JavaScripts
	============================================= -->
	<script src="/static/xsite_template/js/jquery.js"></script>
	<script src="/static/xsite_template/js/plugins.js"></script>

	<script>

		jQuery(document).ready(
			function active_class_function(e) {
				var elems = document.querySelector(".current");
				if (elems !== null) {
					elems.classList.remove("current");
				}
				e.target.className = "current	";
			}
		);

	</script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

 <script>
        $(document).ready(function () {
            $('#template-contactform-phone-buyer').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-phone-seller').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-zip-seller').focus(function () {
                var mask = "99999";
                $(this).inputmask(mask, {"placeholder": ""});
            });
        });
 </script>

</body>"""

    XBrownStone_body_seller="""<body class="stretched">

	<!-- Document Wrapper
	============================================= -->
	<div id="wrapper" class="clearfix">

        <!-- Top Bar
    ============================================= -->
    <div id="top-bar" class="transparent-topbar">

        <div class="container clearfix">


            <div class="col_half fright dark col_last clearfix nobottommargin">

                <!-- Top Social
                ============================================= -->
                <div id="top-social">
                    <ul>
                        <li><a href="#" class="si-facebook" target="_blank"><span class="ts-icon"><i
                                class="fab fa-facebook-f"></i></span><span class="ts-text">Facebook</span></a>
                        </li>
                        <li><a href="#" class="si-twitter" target="_blank"><span class="ts-icon"><i
                                class="fab fa-twitter"></i></span><span class="ts-text">Twitter</span></a>
                        </li>
                        <li><a href="#" class="si-youtube" target="_blank"><span class="ts-icon"><i
                                class="fab fa-youtube"></i></span><span class="ts-text">Youtube</span></a>
                        </li>
                        <li><a href="#" class="si-instagram" target="_blank"><span class="ts-icon"><i
                                class="fab fa-instagram"></i></span><span
                                class="ts-text">Instagram</span></a></li>
                        <li><a href="tel:+10.11.85412542" class="si-call"><span class="ts-icon"><i
                                class="fa fa-phone fa-flip-horizontal"></i></span><span
                                class="ts-text" id="phone">03334455667</span></a></li>
                        <li><a href="mailto:info@xsite.com" class="si-email3"><span class="ts-icon"><i
                                class="fa fa-envelope"></i></span><span
                                class="ts-text" id="email">support@gmail.com</span></a></li>
                    </ul>
                </div><!-- #top-social end -->

            </div>

        </div>

    </div><!-- #top-bar end -->

    <!-- Header
    ============================================= -->
    <header id="header" class="transparent-header floating-header clearfix">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo" data-dark-logo="images/logo-dark.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Xsite Logo"></a>
                    <a href="#" class="retina-logo" data-dark-logo="images/logo-dark@2x.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Xsite Logo"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigationlogo.png
                ============================================= -->
                <nav id="primary-menu" class="with-arrows">

                    <ul onclick="active_class_function(event)">
                        <li class="current"><a href="#">
                            <div>Home</div>
                        </a></li>
                        <li><a href="#about">
                            <div>About</div>
                        </a></li>
                        <li><a href="#get_ebook">
                            <div>Details</div>
                        </a></li>
                        <li><a href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                    </ul>

                    <!-- Menu Buttons
                    ============================================= -->
                    <a href="#get_ebook"
                       class="button button-rounded fright leftmargin-sm banner_button_text">Get Your Ebook</a>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element slider-parallax full-screen clearfix"
             style="background: #FFF url('/static/xsite_template/all_templates/xsite_template_three/images/hero/hero-3.jpg') center center no-repeat; background-size: cover;">

        <div class="vertical-middle">
            <div class="container topmargin-sm">
                <div class="row">
                    <div class="col-lg-6 col-md-8">
                        <div class="slider-title">
                            <h2 id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home
                            Prices. </h2>
                            <a href="#get_ebook"
                               class="button button-rounded button-large nott ls0 banner_button_text">Get Your Ebook</a>
                        </div>
                    </div>
                </div>
            </div>

        </div>


    </section><!-- #slider end -->

    <!-- Content
    ============================================= -->
    <section id="content">

        <div class="content-wrap pt-0 pb-0">

            <!-- Features
            ============================================= -->
            <div class="section nobg mt-4 mb-0 pb-0" id="about" style="padding: 80px 0;">
                <div class="container">
                    <div class="heading-block nobottomborder center divcenter mb-0 clearfix">
                        <div class="badge badge-pill badge-default">About</div>
                        <h3 id="about_us_title" class="nott ls0 mb-3">Little More Detail About Us</h3>
                        <p id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?
                        </p>
                    </div>

                </div>
            </div>

            <!--
            ============================================= -->
            <div class="section m-0" id="get_ebook"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/4.png') no-repeat center top; background-size: cover; padding: 100px 0 0;">
                <div class="container">
                    <div class="row justify-content-between">
                        <div class="col-lg-8  col-md-8 ">
                            <div class="heading-block nobottomborder bottommargin-sm">
                                <div class="badge badge-pill badge-default">More Details</div>
                                <h3 id="other_details_title" class="nott ls0">More To Know Us</h3>
                            </div>
                            <p id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt? </p>
                        </div>

                        <div class="col-lg-4 col-md-4">
                            <div id="section-pricing" class="page-section nopadding nomargin">

                                <div id="pricing-switch"
                                     class="pricing row align-items-end topmargin-sm bottommargin-lg clearfix">
                                    <div class="card shadow-sm">
                                        <div class="card-body">
                                            <h4 class="mb-3"> Get Deals First hand!! Submit your information!</h4>
                                            <div class="form-widget">
                                                <div class="form-result"></div>
                                                    <form id="buyer_form" class="nobottommargin" name="template-contactform"
                                                          method="post">
                                                        <div class="form-process"></div>

                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-name-buyer">Name
                                                                <small>*</small></label>
                                                            <input type="text"
                                                                   name="fullname"
                                                                   id="template-contactform-name-buyer"
                                                                   class="form-control input-sm required"/>
                                                        </div>

                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-email-buyer">Email
                                                                <small>*</small></label>
                                                            <input type="email"
                                                                   name="email"
                                                                   id="template-contactform-email-buyer"
                                                                   class="form-control input-sm required"/>
                                                        </div>

                                                        <div class="clear"></div>

                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-phone-buyer">Phone<small>*</small></label>
                                                            <input type="text" id="template-contactform-phone-buyer"
                                                                   name="phone"
                                                                   class="form-control input-sm required"/>
                                                        </div>
                                                        <div class="col_full mb-4">
                                                            <label for="template-contactform-service-buyer">What are you
                                                                looking
                                                                for?</label>
                                                            <select id="template-contactform-service-buyer"
                                                                    name="what_are_you_looking_for"
                                                                    class="sm-form-control">
                                                                <option value="">What are you looking for?</option>
                                                            </select>

                                                        </div>
                                                        <input type="hidden" name="audience" value="Buyer">
                                                        <div class="col_full nobottommargin">
                                                            <button class="button button-rounded btn-block nott ls0 m-0"
                                                                    type="submit"
                                                                    name="template-contactform-submit"
                                                                    id="template-contactform-submit-buyer"
                                                                    value="submit"> GET Your Ebook

                                                            </button>
                                                        </div>
                                                    </form>
                                                    <form id="seller_form" class="nobottommargin" name="template-contactform"
                                                          method="post">
                                                        <input type="hidden" name="audience" value="Seller">
                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-name-seller">Name
                                                                <small>*</small></label>
                                                            <input type="text" id="template-contactform-name-seller"
                                                                   name="fullname"
                                                                   class="form-control input-sm required"/>
                                                        </div>
                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-phone-seller">Phone<small>*</small></label>
                                                            <input type="text" id="template-contactform-phone-seller"
                                                                   name="phone"
                                                                   class="form-control input-sm required"/>
                                                        </div>
                                                        <div class="col_full mb-3">
                                                            <label for="template-contactform-email-seller">Email
                                                                <small>*</small></label>
                                                            <input type="email" id="template-contactform-email-seller"
                                                                   name="email"
                                                                   class="form-control input-sm required"/>
                                                        </div>

                                                        <div class="col_full mb-3 pt-3">

                                                            <div class="form-check">
                                                                <label class="form-check-label">

                                                                    <input name="immediate_assistance"
                                                                           id="immediate_assistance" type="checkbox"
                                                                           class="form-check-input"
                                                                           onclick="javascript:ShowFields()">
                                                                    I
                                                                    would like
                                                                    immediate assistance
                                                                </label>
                                                            </div>
                                                        </div>

                                                        <div id="immediate_assistance_fields" style="display: none">
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-address-seller">Street
                                                                    Address</label>
                                                                <input type="text"
                                                                       id="template-contactform-address-seller"
                                                                       name="street_address"
                                                                       class="form-control input-sm required"/>
                                                            </div>

                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-city-seller">City</label>
                                                                <input type="text" id="template-contactform-city-seller"
                                                                       name="city"
                                                                       class="form-control input-sm required"/>
                                                            </div>
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-state-seller">State</label>
                                                                <select id="template-contactform-state-seller"
                                                                        name="state"
                                                                        class="sm-form-control">
                                                                    <option value="">State</option>
                                                                    <option value="AL">
                                                                        Alabama
                                                                    </option>
                                                                    <option value="AK">
                                                                        Alaska
                                                                    </option>
                                                                    <option value="AB">
                                                                        Alberta
                                                                    </option>
                                                                    <option value="AS">
                                                                        American Samoa
                                                                    </option>
                                                                    <option value="AZ">
                                                                        Arizona
                                                                    </option>
                                                                    <option value="AR">
                                                                        Arkansas
                                                                    </option>
                                                                    <option value="BC">
                                                                        British Columbia
                                                                    </option>
                                                                    <option value="CA">
                                                                        California
                                                                    </option>
                                                                    <option value="CO">
                                                                        Colorado
                                                                    </option>
                                                                    <option value="CT">
                                                                        Connecticut
                                                                    </option>
                                                                    <option value="DE">
                                                                        Delaware
                                                                    </option>
                                                                    <option value="FM">
                                                                        Fed. St. of Micronesia
                                                                    </option>
                                                                    <option value="FL">
                                                                        Florida
                                                                    </option>
                                                                    <option value="GA">
                                                                        Georgia
                                                                    </option>
                                                                    <option value="GU">
                                                                        Guam
                                                                    </option>
                                                                    <option value="HI">
                                                                        Hawaii
                                                                    </option>
                                                                    <option value="ID">
                                                                        Idaho
                                                                    </option>
                                                                    <option value="IL">
                                                                        Illinois
                                                                    </option>
                                                                    <option value="IN">
                                                                        Indiana
                                                                    </option>
                                                                    <option value="IA">
                                                                        Iowa
                                                                    </option>
                                                                    <option value="KS">
                                                                        Kansas
                                                                    </option>
                                                                    <option value="KY">
                                                                        Kentucky
                                                                    </option>
                                                                    <option value="LA">
                                                                        Louisiana
                                                                    </option>
                                                                    <option value="ME">
                                                                        Maine
                                                                    </option>
                                                                    <option value="MB">
                                                                        Manitoba
                                                                    </option>
                                                                    <option value="MH">
                                                                        Marshall Islands
                                                                    </option>
                                                                    <option value="MD">
                                                                        Maryland
                                                                    </option>
                                                                    <option value="MA">
                                                                        Massachusetts
                                                                    </option>
                                                                    <option value="MI">
                                                                        Michigan
                                                                    </option>
                                                                    <option value="MN">
                                                                        Minnesota
                                                                    </option>
                                                                    <option value="MS">
                                                                        Mississippi
                                                                    </option>
                                                                    <option value="MO">
                                                                        Missouri
                                                                    </option>
                                                                    <option value="MT">
                                                                        Montana
                                                                    </option>
                                                                    <option value="NE">
                                                                        Nebraska
                                                                    </option>
                                                                    <option value="NV">
                                                                        Nevada
                                                                    </option>
                                                                    <option value="NB">
                                                                        New Brunswick
                                                                    </option>
                                                                    <option value="NH">
                                                                        New Hampshire
                                                                    </option>
                                                                    <option value="NJ">
                                                                        New Jersey
                                                                    </option>
                                                                    <option value="NM">
                                                                        New Mexico
                                                                    </option>
                                                                    <option value="NY">
                                                                        New York
                                                                    </option>
                                                                    <option value="NL">
                                                                        Newfoundland
                                                                    </option>
                                                                    <option value="NC">
                                                                        North Carolina
                                                                    </option>
                                                                    <option value="ND">
                                                                        North Dakota
                                                                    </option>
                                                                    <option value="MP">
                                                                        Northern Mariana Islands
                                                                    </option>
                                                                    <option value="NT">
                                                                        Northwest Territory
                                                                    </option>
                                                                    <option value="NS">
                                                                        Nova Scotia
                                                                    </option>
                                                                    <option value="NU">
                                                                        Nunavut
                                                                    </option>
                                                                    <option value="OH">
                                                                        Ohio
                                                                    </option>
                                                                    <option value="OK">
                                                                        Oklahoma
                                                                    </option>
                                                                    <option value="ON">
                                                                        Ontario
                                                                    </option>
                                                                    <option value="OR">
                                                                        Oregon
                                                                    </option>
                                                                    <option value="PA">
                                                                        Pennsylvania
                                                                    </option>
                                                                    <option value="PE">
                                                                        Prince Edward Island
                                                                    </option>
                                                                    <option value="PR">
                                                                        Puerto Rico
                                                                    </option>
                                                                    <option value="QC">
                                                                        Quebec
                                                                    </option>
                                                                    <option value="RI">
                                                                        Rhode Island
                                                                    </option>
                                                                    <option value="SK">
                                                                        Saskatchewan
                                                                    </option>
                                                                    <option value="SC">
                                                                        South Carolina
                                                                    </option>
                                                                    <option value="SD">
                                                                        South Dakota
                                                                    </option>
                                                                    <option value="TN">
                                                                        Tennessee
                                                                    </option>
                                                                    <option value="TX">
                                                                        Texas
                                                                    </option>
                                                                    <option value="UT">
                                                                        Utah
                                                                    </option>
                                                                    <option value="VT">
                                                                        Vermont
                                                                    </option>
                                                                    <option value="VI">
                                                                        Virgin Islands
                                                                    </option>
                                                                    <option value="VA">
                                                                        Virginia
                                                                    </option>
                                                                    <option value="WA">
                                                                        Washington
                                                                    </option>
                                                                    <option value="DC">
                                                                        Washington DC
                                                                    </option>
                                                                    <option value="WV">
                                                                            West Virginia
                                                                    </option>
                                                                    <option value="WI">
                                                                        Wisconsin
                                                                    </option>
                                                                    <option value="WY">
                                                                        Wyoming
                                                                    </option>
                                                                    <option value="YT">
                                                                        Yukon Territory
                                                                    </option>
                                                                </select>
                                                            </div>
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-zip-seller">Zip/Postal
                                                                    Code</label>
                                                                <input type="text" id="template-contactform-zip-seller"
                                                                       name="zip"
                                                                       class="form-control input-sm required"/>

                                                            </div>
                                                            <div class="col_full mb-3">
                                                                <label for="template-contactform-is_home_listed-seller">
                                                                    Is
                                                                    home listed?</label>
                                                                <select id="template-contactform-is_home_listed-seller"
                                                                        name="is_home_listed" class="sm-form-control">
                                                                    <option value="">Is home listed?</option>
                                                                </select>
                                                            </div>
                                                            <div class="col_full mb-4">
                                                                <label for="template-contactform-asking_price-seller">Asking
                                                                    Price</label>
                                                                <input type="number"
                                                                       id="template-contactform-asking_price-seller"
                                                                       name="asking_price"
                                                                       class="form-control input-sm required" min="0"/>
                                                            </div>
                                                        </div>


                                                        <div class="col_full nobottommargin">
                                                            <button class="button button-rounded btn-block nott ls0 m-0"
                                                                    type="submit"
                                                                    name="template-contactform-submit"
                                                                    id="template-contactform-seller"
                                                                    value="submit"> GET youur ebook
                                                            </button>
                                                        </div>
                                                    </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>
            </div>

            <!-- Form Section
            ============================================= -->
            <div class="section m-0"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/1.jpg') no-repeat center center; background-size: cover; padding: 100px 0;">
                <div class="container">
                    <div class="row justify-content-between align-items-center">

                        <div class="col-md-6">
                            <div class="heading-block nobottomborder bottommargin-sm">
                                <h3 id="video_title" class="nott ls0">Title</h3>
                            </div>
                            <p id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt? </p>

                        </div>


                        <div class="col-md-4 mt-5 mt-md-0 center">
                            <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe"
                               class="play-icon shadow"><i class="fa fa-play"></i></a>
                        </div>

                    </div>

                </div>
            </div>


            <!-- Testimonials
            ============================================= -->
            <div class="section mt-0" id="testimonails"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/sections/3.jpg') no-repeat top center; background-size: cover; padding: 80px 0 70px;">
                <div class="container">
                    <div class="heading-block nobottomborder center">
                        <div class="badge badge-pill badge-default">Testimonials</div>
                        <h3 class="nott ls0">What Clients Says</h3>
                    </div>

                    <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget clearfix"
                         data-margin="0" data-pagi="true" data-loop="true" data-center="true" data-autoplay="5000"
                         data-items-sm="1" data-items-md="2" data-items-xl="3">

                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-image">
                                    <a href="#"><img
                                            src="/static/xsite_template/all_templates/xsite_template_three/images/avatar.png"
                                            alt="Customer Testimonails"></a>
                                </div>
                                <div class="testi-content">
                                    <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_1_person_name">Person 1</span>
                                        <span id="testi_1_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="oc-item">
                                <div class="testimonial">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_three/images/avatar.png"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_2_person_name">Person 1</span>
                                            <span id="testi_2_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="oc-item">
                                <div class="testimonial">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_three/images/avatar.png"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_3_person_name">Person 1</span>
                                            <span id="testi_3_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                    </div>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="noborder bg-white">
        <!-- Copyrights
        ============================================= -->
        <div id="copyrights"
             style="background: url('/static/xsite_template/all_templates/xsite_template_three/images/hero/footer.svg') no-repeat top center; background-size: cover; padding-top: 70px;">
            <div class="container clearfix">
                <div class="col_half">
                    &copy; 2020 <a target="_blank" href="https://prospectx.com/">Prospectx</a> All Rights Reserved.
                </div>
            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->


</div><!-- #wrapper end -->

	<!-- Go To Top
	============================================= -->
	<div id="gotoTop" class="fa fa-angle-up"></div>

	<!-- External JavaScripts
	============================================= -->
	<script src="/static/xsite_template/js/jquery.js"></script>
	<script src="/static/xsite_template/js/plugins.js"></script>

	<script>

		jQuery(document).ready(
			function active_class_function(e) {
				var elems = document.querySelector(".current");
				if (elems !== null) {
					elems.classList.remove("current");
				}
				e.target.className = "current	";
			}
		);

	</script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

 <script>
        $(document).ready(function () {
            $('#template-contactform-phone-buyer').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-phone-seller').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-zip-seller').focus(function () {
                var mask = "99999";
                $(this).inputmask(mask, {"placeholder": ""});
            });
        });
 </script>

</body>"""

    Modernistic_head = """<head> 	<meta http-equiv="content-type" content="text/html; charset=utf-8"/>     <meta name="author" content="SemiColonWeb"/>        <title>Xsite</title>      <!-- Stylesheets     ============================================= -->     <link href="http://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,900|Caveat+Brush" rel="stylesheet"           type="text/css"/>     <link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css"/>     <link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css"/>      <link rel="stylesheet" href="/static/xsite_template/css/swiper.css" type="text/css"/>      <link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css"/>     <link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css"/>     <link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css"/>     <link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css"/>      <link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css"/>     <link rel="stylesheet" href="/static/xsite_template/css/calendar.css" type="text/css"/>      <!-- NonProfit Demo Specific Stylesheet -->     <link rel="stylesheet" href="/static/xsite_template/css/colors.php?color=C6C09C" type="text/css"/>     <!-- Theme Color -->     <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_four/css/fonts.css"           type="text/css"/>     <link rel="stylesheet"           href="/static/xsite_template/all_templates/xsite_template_four/xsite_template_four.css"           type="text/css"/>     <!-- / -->      <meta name='viewport' content='initial-scale=1, viewport-fit=cover'>
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">     <!-- / --> </head>"""
    Modernistic_body = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">
 <!-- Header
    ============================================= -->
    <header id="header" class="clearfix static-sticky">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo" data-dark-logo="images/prospectx-logo.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="xsite Logo"></a>
                    <a href="#" class="retina-logo" data-dark-logo="images/prospectx-logo.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="xsite Logo"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu"
                     class="d-lg-flex d-xl-flex justify-content-xl-between justify-content-lg-between fnone with-arrows">


                    <ul class="align-self-start">
                        <li><span class="menu-bg col-auto align-self-start d-flex"></span></li>
                        <li class="active"><a href="#home">
                            <div>Home</div>
                        </a></li>
                        <li><a href="#about">
                            <div>About</div>
                        </a>
                        </li>
                        <li><a href="#details">
                            <div>Details</div>
                        </a></li>
                        <li><a href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                    </ul>

                    <ul class="not-dark align-self-end">
                        <li><a href="#details" class="header-button">
                            <div class="banner_button_text">Get your ebook</div>
                        </a></li>
                    </ul>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="home"
             class="slider-element dark swiper_wrapper full-screen force-full-screen slider-parallax clearfix">

        <div class="slider-parallax-inner">

            <div class="swiper-container swiper-parent">
                <div class="swiper-wrapper">
                    <div class="swiper-slide dark"
                         style="background: linear-gradient(rgba(0,0,0,.3), rgba(0,0,0,.5)), url('/static/xsite_template/all_templates/xsite_template_four/images/slider/3.jpg') no-repeat center center; background-size: cover;">
                        <div class="container clearfix">
                            <div class="slider-caption">
                                <h2 class="nott" data-animate="fadeInUp" id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home Prices.</h2>
                                <p style="font-size: 17px;" data-animate="fadeInUp" data-delay="200">We give FAIR cash offers for your home! Give us a call today or fill out one of the forms on our website! </p>
                                <a href="#details" data-animate="fadeInUp" data-delay="400"
                                   class="button button-rounded button-large button-light text-dark bgcolor shadow nott ls0 ml-0 mt-4 banner_button_text">Get your book</a>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <div class="swiper-scrollbar">
                    <div class="swiper-scrollbar-drag">
                        <div class="slide-number">
                            <div class="slide-number-current"></div>
                            <span>/</span>
                            <div class="slide-number-total"></div>
                        </div>
                    </div>
                </div> -->
            </div>

        </div>

    </section>

    <!-- Content
    ============================================= -->
    <section id="content" style="overflow: visible">

        <div class="content-wrap p-0" id="about">

            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1382 58" width="100%" height="60"
                 preserveAspectRatio="none" style="position: absolute; top: -58px; left:0; z-index: 1">
                <path style="fill:#FFF;" d="M1.52.62s802.13,127,1380,0v56H.51Z"></path>
            </svg>

            <div class="container clearfix">

                <div class="slider-feature w-100">
                    <div class="row justify-content-center">
                        <div class="col-md-3 px-1">
                            <a href="#"
                               class="card center border-left-0 border-right-0 border-top-0 border-bottom border-bottom shadow py-3 noradius t600 uppercase ls1">
                                <div class="card-body">
                                    <i class="fa fa-align-center"></i> Our Mission
                                </div>
                            </a>
                        </div>
                        <div class="col-md-3 px-1">
                            <a href="#"
                               class="card center border-left-0 border-right-0 border-top-0 border-bottom border-bottom shadow py-3 noradius t600 uppercase ls1">
                                <div class="card-body">
                                    <i class="fa fa-umbrella"></i>Testimonials
                                </div>
                            </a>
                        </div>
                        <div class="col-md-3 px-1">
                            <a href="#"
                               class="card center border-left-0 border-right-0 border-top-0 border-bottom border-bottom shadow py-3 noradius t600 uppercase ls1">
                                <div class="card-body">
                                    <i class="fa fa-envelope"></i> <span class="banner_button_text">Get your ebook</span>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>

            </div>

            <div class="section mt-3">
                <div class="container clearfix">
                    <div class="row justify-content-center">
                        <div class="col-md-10 center">
                            <div class="heading-block nobottomborder mb-4">
                                <h2 class="mb-4 nott" id="about_us_title">Little More Detail About Us</h2>
                            </div>
                            <div class="svg-line bottommargin-sm clearfix">
                                <img src="/static/xsite_template/all_templates/xsite_template_four/images/divider-1.svg"
                                     alt="svg divider" height="20">
                            </div>
                            <p id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt? </p>
                        </div>
                    </div>

                </div>
            </div>

            <div class="container">
                <div class="w-100 position-relative">
                    <div class="donor-img d-flex align-items-center rounded parallax divcenter shadow-sm"
                         data-bottom-top="background-position:0px 0px;" data-top-bottom="background-position:0px -50px;"
                         style="max-width: 1100px; width: 100%; height: 500px; background: url('/static/xsite_template/all_templates/xsite_template_four/images/others/rental-house-image.jpeg') no-repeat center center / cover"></div>
                    <div class="card bg-white border-0 center py-sm-4 px-sm-5 p-2 shadow-sm"
                         style="position: absolute; top: 50%; right: 80px; transform: translateY(-50%);">
                        <div class="card-body">
                            <div class="color h1 mb-3"><i class="text-dark far fa-heart"></i></div>
                            <small class="uppercase t400 ls2 text-muted mb-3 d-block">Our top clients</small>
                            <h3 class="display-3 t700 mb-3 font-secondary">2.4M</h3>
                        </div>
                    </div>
                </div>
            </div>

            <div class="clear"></div>

            <div class="section"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_four/images/others/section-bg.jpg') no-repeat center center / cover; padding: 80px 0;">
                <div class="container clearfix">
                    <div class="row">
                        <div class="col-lg-8">
                            <h3 class="mb-2" id="video_title">Video </h3>
                            <div class="svg-line mb-2 clearfix">
                                <img src="/static/xsite_template/all_templates/xsite_template_four/images/divider-1.svg"
                                     alt="svg divider"
                                     height="10">
                            </div>
                            <p class="mb-5" id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</p>

                        </div>

                        <div class="col-lg-4 mt-5 mt-lg-0">
                            <h3 class="mb-2">Latest Videos</h3>

                            <div class="clear"></div>
                            <a  id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe"
                               class="shadow-sm d-flex align-items-center justify-content-center play-video rounded position-relative bg-color mt-3 clearfix"
                               style="background: linear-gradient(rgba(0,0,0,.05), rgba(0,0,0,.01)), url('/static/xsite_template/all_templates/xsite_template_four/images/others/8.jpg') no-repeat center center / cover; height: 300px"><i
                                    class="fa fa-play"></i></a>

                        </div>
                    </div>
                </div>
            </div>

            <div class="section nobg" id="details">
                <div class="container clearfix">
                    <div class="row justify-content-center mb-5">
                        <div class="col-md-10 center">
                            <div class="heading-block nobottomborder mb-4">
                                <h2 class="mb-4 nott" id="other_details_title">More To Know Us</h2>
                            </div>
                            <div class="svg-line bottommargin-sm clearfix">
                                <img src="/static/xsite_template/all_templates/xsite_template_four/images/divider-1.svg"
                                     alt="svg divider"
                                     height="20">
                            </div>
                            <p id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bgcolor subscribe-section position-relative" style="margin-top: 100px;" >
                <div class="container" style="z-index: 2;">
                    <div class="center collapsed subscribe-section-target" data-toggle="collapse"
                         data-target="#target-1">
                        <div class="subscribe-icon"><i class="fa fa-envelope"></i></div>
                        <h2 class="mb-0 mt-2 position-relative" style="z-index: 1;" id="banner_title1">Find Your Dream Home Here! Beautiful Homes At Ugly Home Prices.
                            <i class="fa fa-arrow-down position-relative" style="top: 5px"></i>
                        </h2>
                    </div>
                    <div class="collapse show" id="target-1">
                        <div class="form-widget pb-5" data-alert-type="false">

                            <div class="form-result"></div>

                            <div class="nonprofit-loader css3-spinner" style="position: absolute;">
                                <div class="css3-spinner-bounce1"></div>
                                <div class="css3-spinner-bounce2"></div>
                                <div class="css3-spinner-bounce3"></div>
                            </div>
                            <div id="nonprofit-submitted" class="center">
                                <h4 class="t600 mb-0">Thank You for Contact Us! Our Team will contact you asap on your
                                    email Address.</h4>
                            </div>
                                <form id="buyer_form" class="row mt-2" method="post">
                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-name-buyer">Name <small>*</small></label>
                                        <input type="text"
                                               name="fullname"
                                               id="template-contactform-name-buyer"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Full Name">
                                    </div>

                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-email-buyer">Email <small>*</small></label>
                                        <input type="email" name="email"
                                               id="template-contactform-email-buyer"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Email"/>
                                    </div>

                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-phone-buyer">Phone<small>*</small></label>
                                        <input type="text" name="phone" id="template-contactform-phone-buyer"
                                               class="form-control border-form-control"
                                               placeholder="Enter your Contact Number">
                                    </div>
                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-service-buyer">What are you looking
                                            for?</label>
                                        <select id="template-contactform-service-buyer"
                                                name="what_are_you_looking_for"
                                                class="form-control border-form-control">
                                            <option value="">What are you looking for?</option>
                                        </select>

                                    </div>
                                    <input type="hidden" name="audience" value="Buyer">
                                    <button class="btn button button-rounded button-xlarge button-dark bg-dark shadow nott ls0 m-0 subscribe-button"
                                            type="submit"
                                            name="template-contactform-submit"
                                            id="template-contactform-submit-buyer"
                                            value="submit"> Get your book
                                    </button>

                                </form>
                                <form id="seller_form" class="row mt-2" method="post">
                                    <div class="col-md-4 mb-4 mb-md-1">
                                        <label for="template-contactform-name-seller">Name <small>*</small></label>
                                        <input type="text"
                                               name="fullname"
                                               id="template-contactform-name-seller"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Full Name">
                                    </div>

                                    <div class="col-md-4 mb-4 mb-md-1">
                                        <label for="template-contactform-email-seller">Email <small>*</small></label>
                                        <input type="email"
                                               name="email"
                                               id="template-contactform-email-seller"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Email"/>
                                    </div>

                                    <div class="col-md-4 mb-4 mb-md-1">
                                        <label for="template-contactform-phone-seller">Phone<small>*</small></label>
                                        <input type="text" name="phone" id="template-contactform-phone-seller"
                                               class="form-control border-form-control"
                                               placeholder="Enter your Contact Number">
                                    </div>
                                    <div class="col-md-12 mb-4 mb-md-3 mt-3 text-center">
                                        <div class="form-check">
                                            <label class="form-check-label">

                                                <input name="immediate_assistance" id="immediate_assistance"
                                                       type="checkbox"
                                                       class="form-check-input" onclick="javascript:ShowFields()">
                                                I
                                                would like
                                                immediate assistance
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-12 mb-4 mb-md-1">
                                        <div id="immediate_assistance_fields" style="display: none">
                                            <div class="row">
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-address-seller">Street
                                                        Address</label>
                                                    <input type="text" id="template-contactform-address-seller"
                                                           name="street_address"
                                                           class="form-control border-form-control required"
                                                           placeholder="Enter Your Street Address.."/>
                                                </div>

                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-city-seller">City</label>
                                                    <input type="text" id="template-contactform-city-seller"
                                                           name="city"
                                                           class="form-control border-form-control required"
                                                           placeholder="Enter Your City.."/>
                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-state-seller">State</label>
                                                    <select id="template-contactform-state-seller" name="state"
                                                            class="form-control border-form-control">
                                                        <option value="">State</option>
                                                        <option value="AL">
                                                            Alabama
                                                        </option>
                                                        <option value="AK">
                                                            Alaska
                                                        </option>
                                                        <option value="AB">
                                                            Alberta
                                                        </option>
                                                        <option value="AS">
                                                            American Samoa
                                                        </option>
                                                        <option value="AZ">
                                                            Arizona
                                                        </option>
                                                        <option value="AR">
                                                            Arkansas
                                                        </option>
                                                        <option value="BC">
                                                            British Columbia
                                                        </option>
                                                        <option value="CA">
                                                            California
                                                        </option>
                                                        <option value="CO">
                                                            Colorado
                                                        </option>
                                                        <option value="CT">
                                                            Connecticut
                                                        </option>
                                                        <option value="DE">
                                                            Delaware
                                                        </option>
                                                        <option value="FM">
                                                            Fed. St. of Micronesia
                                                        </option>
                                                        <option value="FL">
                                                            Florida
                                                        </option>
                                                        <option value="GA">
                                                            Georgia
                                                        </option>
                                                        <option value="GU">
                                                            Guam
                                                        </option>
                                                        <option value="HI">
                                                            Hawaii
                                                        </option>
                                                        <option value="ID">
                                                            Idaho
                                                        </option>
                                                        <option value="IL">
                                                            Illinois
                                                        </option>
                                                        <option value="IN">
                                                            Indiana
                                                        </option>
                                                        <option value="IA">
                                                            Iowa
                                                        </option>
                                                        <option value="KS">
                                                            Kansas
                                                        </option>
                                                        <option value="KY">
                                                            Kentucky
                                                        </option>
                                                        <option value="LA">
                                                            Louisiana
                                                        </option>
                                                        <option value="ME">
                                                            Maine
                                                        </option>
                                                        <option value="MB">
                                                            Manitoba
                                                        </option>
                                                        <option value="MH">
                                                            Marshall Islands
                                                        </option>
                                                        <option value="MD">
                                                            Maryland
                                                        </option>
                                                        <option value="MA">
                                                            Massachusetts
                                                        </option>
                                                        <option value="MI">
                                                            Michigan
                                                        </option>
                                                        <option value="MN">
                                                            Minnesota
                                                        </option>
                                                        <option value="MS">
                                                            Mississippi
                                                        </option>
                                                        <option value="MO">
                                                            Missouri
                                                        </option>
                                                        <option value="MT">
                                                            Montana
                                                        </option>
                                                        <option value="NE">
                                                            Nebraska
                                                        </option>
                                                        <option value="NV">
                                                            Nevada
                                                        </option>
                                                        <option value="NB">
                                                            New Brunswick
                                                        </option>
                                                        <option value="NH">
                                                            New Hampshire
                                                        </option>
                                                        <option value="NJ">
                                                            New Jersey
                                                        </option>
                                                        <option value="NM">
                                                            New Mexico
                                                        </option>
                                                        <option value="NY">
                                                            New York
                                                        </option>
                                                        <option value="NL">
                                                            Newfoundland
                                                        </option>
                                                        <option value="NC">
                                                            North Carolina
                                                        </option>
                                                        <option value="ND">
                                                            North Dakota
                                                        </option>
                                                        <option value="MP">
                                                            Northern Mariana Islands
                                                        </option>
                                                        <option value="NT">
                                                            Northwest Territory
                                                        </option>
                                                        <option value="NS">
                                                            Nova Scotia
                                                        </option>
                                                        <option value="NU">
                                                            Nunavut
                                                        </option>
                                                        <option value="OH">
                                                            Ohio
                                                        </option>
                                                        <option value="OK">
                                                            Oklahoma
                                                        </option>
                                                        <option value="ON">
                                                            Ontario
                                                        </option>
                                                        <option value="OR">
                                                            Oregon
                                                        </option>
                                                        <option value="PA">
                                                            Pennsylvania
                                                        </option>
                                                        <option value="PE">
                                                            Prince Edward Island
                                                        </option>
                                                        <option value="PR">
                                                            Puerto Rico
                                                        </option>
                                                        <option value="QC">
                                                            Quebec
                                                        </option>
                                                        <option value="RI">
                                                            Rhode Island
                                                        </option>
                                                        <option value="SK">
                                                            Saskatchewan
                                                        </option>
                                                        <option value="SC">
                                                            South Carolina
                                                        </option>
                                                        <option value="SD">
                                                            South Dakota
                                                        </option>
                                                        <option value="TN">
                                                            Tennessee
                                                        </option>
                                                        <option value="TX">
                                                            Texas
                                                        </option>
                                                        <option value="UT">
                                                            Utah
                                                        </option>
                                                        <option value="VT">
                                                            Vermont
                                                        </option>
                                                        <option value="VI">
                                                            Virgin Islands
                                                        </option>
                                                        <option value="VA">
                                                            Virginia
                                                        </option>
                                                        <option value="WA">
                                                            Washington
                                                        </option>
                                                        <option value="DC">
                                                            Washington DC
                                                        </option>
                                                        <option value="WV">
                                                                West Virginia
                                                        </option>
                                                        <option value="WI">
                                                            Wisconsin
                                                        </option>
                                                        <option value="WY">
                                                            Wyoming
                                                        </option>
                                                        <option value="YT">
                                                            Yukon Territory
                                                        </option>
                                                    </select>
                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-zip-seller">Zip/Postal Code</label>
                                                    <input type="text" id="template-contactform-zip-seller"
                                                           name="zip" placeholder="Enter Your Zip.."
                                                           class="form-control border-form-control required"/>

                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-is_home_listed-seller"> Is home
                                                        listed?</label>
                                                    <select id="template-contactform-is_home_listed-seller"
                                                            name="is_home_listed"
                                                            class="form-control border-form-control">
                                                        <option value="">Is home listed?</option>
                                                    </select>
                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-asking_price-seller">Asking
                                                        Price</label>
                                                    <input type="number" id="template-contactform-asking_price-seller"
                                                           name="asking_price" placeholder="Enter Your Asking Price.."
                                                           class="form-control border-form-control required" min="0"/>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <button class="btn button button-rounded button-xlarge button-dark bg-dark shadow nott ls0 m-0 subscribe-button"
                                            type="submit"
                                            name="template-contactform-submit"
                                            id="template-contactform-seller"
                                            value="submit"> Get your book
                                    </button>

                                </form>
                        </div>
                    </div>
                </div>
                <div style="background-image: url('/static/xsite_template/all_templates/xsite_template_four/images/divider-4.svg'); position: absolute; bottom: -20px; left: 0; width: 100%; height: 60px; z-index: 1;"></div>
            </div>

            <div class="line line-sm my-0 clearfix"></div>
            <div class="clear"></div>
            <div class="section section-details mb-0 bg-white" style="padding: 80px 0 80px;" id="testimonials">
                <div class="container clearfix">
                    <div class="row">
                        <div class="col-md-4 px-4 mb-2">
                            <h4 class="t500 mb-4">Contact Us</h4>
                            <abbr title="Phone Number"><strong>Phone:</strong></abbr> <span id="phone">03334455667</span><br>
                            <abbr title="Email Address"><strong>Email:</strong></abbr> <span id="email">support@gmail.com</span>
                        </div>
                        <div class="col-md-6 px-4 mb-5 mb-md-0">
                            <h4 class="t500 mb-3">Testimonials</h4>
                            <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget"
                                 data-margin="0" data-nav="false" data-pagi="false" data-items="1" data-autoplay="6000"
                                 data-loop="true" data-animate-in="fadeIn" data-animate-out="fadeOut">

                                <div class="oc-item">
                                    <div class="testimonial nobg noshadow noborder p-0">
                                        <div class="testi-content">
                                            <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                            <div class="testi-meta ls1" id="testi_1_person_name"> Person 1</div>
                                        </div>
                                    </div>
                                </div>
                                    <div class="oc-item">
                                        <div class="testimonial nobg noshadow noborder p-0">
                                            <div class="testi-content">
                                                <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                <div class="testi-meta ls1" id="testi_2_person_name"> Person 2</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="oc-item">
                                        <div class="testimonial nobg noshadow noborder p-0">
                                            <div class="testi-content">
                                                <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                <div class="testi-meta ls1" id="testi_3_person_name"> Person 3</div>
                                            </div>
                                        </div>
                                    </div>

                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer">


        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="bgcolor pb-2 pt-2">

            <div class="container clearfix">

                <div class="row justify-content-between align-items-center">
                    <div class="col-md-12 text-center">
                        &copy; 2020 <a class="text-dark" target="_blank" href="https://prospectx.com/">Prospectx</a>
                        All Rights Reserved.
                    </div>

                </div>

            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->

</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>
<script src="/static/xsite_template/js/jquery.calendario.js"></script>
<script src="/static/xsite_template/all_templates/xsite_template_four/js/events.js"></script>

<script>
    jQuery(document).ready(function ($) {
        $(".carousel-widget").owlCarousel({
            loop: true,
            items: 1
        });
        var elementParent = $('.floating-contact-wrap');
        $('.floating-contact-btn').off('click').on('click', function () {
            elementParent.toggleClass('active',);
        });
    });

</script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

 <script>
        $(document).ready(function () {
            $('#template-contactform-phone-buyer').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-phone-seller').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-zip-seller').focus(function () {
                var mask = "99999";
                $(this).inputmask(mask, {"placeholder": ""});
            });
        });
 </script>

</body>"""

    Modernistic_body_seller = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">
 <!-- Header
    ============================================= -->
    <header id="header" class="clearfix static-sticky">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo" data-dark-logo="images/prospectx-logo.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="xsite Logo"></a>
                    <a href="#" class="retina-logo" data-dark-logo="images/prospectx-logo.png"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png" alt="xsite Logo"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu"
                     class="d-lg-flex d-xl-flex justify-content-xl-between justify-content-lg-between fnone with-arrows">


                    <ul class="align-self-start">
                        <li><span class="menu-bg col-auto align-self-start d-flex"></span></li>
                        <li class="active"><a href="#home">
                            <div>Home</div>
                        </a></li>
                        <li><a href="#about">
                            <div>About</div>
                        </a>
                        </li>
                        <li><a href="#details">
                            <div>Details</div>
                        </a></li>
                        <li><a href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                    </ul>

                    <ul class="not-dark align-self-end">
                        <li><a href="#details" class="header-button">
                            <div class="banner_button_text">Get your ebook</div>
                        </a></li>
                    </ul>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="home"
             class="slider-element dark swiper_wrapper full-screen force-full-screen slider-parallax clearfix">

        <div class="slider-parallax-inner">

            <div class="swiper-container swiper-parent">
                <div class="swiper-wrapper">
                    <div class="swiper-slide dark"
                         style="background: linear-gradient(rgba(0,0,0,.3), rgba(0,0,0,.5)), url('/static/xsite_template/all_templates/xsite_template_four/images/slider/3.jpg') no-repeat center center; background-size: cover;">
                        <div class="container clearfix">
                            <div class="slider-caption">
                                <h2 class="nott" data-animate="fadeInUp" id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home Prices.</h2>
                                <p style="font-size: 17px;" data-animate="fadeInUp" data-delay="200">Get Deals First hand!! Give us a call today or fill out one of the forms on our website! </p>
                                <a href="#details" data-animate="fadeInUp" data-delay="400"
                                   class="button button-rounded button-large button-light text-dark bgcolor shadow nott ls0 ml-0 mt-4 banner_button_text">Get your book</a>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <div class="swiper-scrollbar">
                    <div class="swiper-scrollbar-drag">
                        <div class="slide-number">
                            <div class="slide-number-current"></div>
                            <span>/</span>
                            <div class="slide-number-total"></div>
                        </div>
                    </div>
                </div> -->
            </div>

        </div>

    </section>

    <!-- Content
    ============================================= -->
    <section id="content" style="overflow: visible">

        <div class="content-wrap p-0" id="about">

            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1382 58" width="100%" height="60"
                 preserveAspectRatio="none" style="position: absolute; top: -58px; left:0; z-index: 1">
                <path style="fill:#FFF;" d="M1.52.62s802.13,127,1380,0v56H.51Z"></path>
            </svg>

            <div class="container clearfix">

                <div class="slider-feature w-100">
                    <div class="row justify-content-center">
                        <div class="col-md-3 px-1">
                            <a href="#"
                               class="card center border-left-0 border-right-0 border-top-0 border-bottom border-bottom shadow py-3 noradius t600 uppercase ls1">
                                <div class="card-body">
                                    <i class="fa fa-align-center"></i> Our Mission
                                </div>
                            </a>
                        </div>
                        <div class="col-md-3 px-1">
                            <a href="#"
                               class="card center border-left-0 border-right-0 border-top-0 border-bottom border-bottom shadow py-3 noradius t600 uppercase ls1">
                                <div class="card-body">
                                    <i class="fa fa-umbrella"></i>Testimonials
                                </div>
                            </a>
                        </div>
                        <div class="col-md-3 px-1">
                            <a href="#"
                               class="card center border-left-0 border-right-0 border-top-0 border-bottom border-bottom shadow py-3 noradius t600 uppercase ls1">
                                <div class="card-body">
                                    <i class="fa fa-envelope"></i> <span class="banner_button_text">Get your ebook</span>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>

            </div>

            <div class="section mt-3">
                <div class="container clearfix">
                    <div class="row justify-content-center">
                        <div class="col-md-10 center">
                            <div class="heading-block nobottomborder mb-4">
                                <h2 class="mb-4 nott" id="about_us_title">Little More Detail About Us</h2>
                            </div>
                            <div class="svg-line bottommargin-sm clearfix">
                                <img src="/static/xsite_template/all_templates/xsite_template_four/images/divider-1.svg"
                                     alt="svg divider" height="20">
                            </div>
                            <p id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt? </p>
                        </div>
                    </div>

                </div>
            </div>

            <div class="container">
                <div class="w-100 position-relative">
                    <div class="donor-img d-flex align-items-center rounded parallax divcenter shadow-sm"
                         data-bottom-top="background-position:0px 0px;" data-top-bottom="background-position:0px -50px;"
                         style="max-width: 1100px; width: 100%; height: 500px; background: url('/static/xsite_template/all_templates/xsite_template_four/images/others/rental-house-image.jpeg') no-repeat center center / cover"></div>
                    <div class="card bg-white border-0 center py-sm-4 px-sm-5 p-2 shadow-sm"
                         style="position: absolute; top: 50%; right: 80px; transform: translateY(-50%);">
                        <div class="card-body">
                            <div class="color h1 mb-3"><i class="text-dark far fa-heart"></i></div>
                            <small class="uppercase t400 ls2 text-muted mb-3 d-block">Our top clients</small>
                            <h3 class="display-3 t700 mb-3 font-secondary">2.4M</h3>
                        </div>
                    </div>
                </div>
            </div>

            <div class="clear"></div>

            <div class="section"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_four/images/others/section-bg.jpg') no-repeat center center / cover; padding: 80px 0;">
                <div class="container clearfix">
                    <div class="row">
                        <div class="col-lg-8">
                            <h3 class="mb-2" id="video_title">Video </h3>
                            <div class="svg-line mb-2 clearfix">
                                <img src="/static/xsite_template/all_templates/xsite_template_four/images/divider-1.svg"
                                     alt="svg divider"
                                     height="10">
                            </div>
                            <p class="mb-5" id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</p>

                        </div>

                        <div class="col-lg-4 mt-5 mt-lg-0">
                            <h3 class="mb-2">Latest Videos</h3>

                            <div class="clear"></div>
                            <a  id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe"
                               class="shadow-sm d-flex align-items-center justify-content-center play-video rounded position-relative bg-color mt-3 clearfix"
                               style="background: linear-gradient(rgba(0,0,0,.05), rgba(0,0,0,.01)), url('/static/xsite_template/all_templates/xsite_template_four/images/others/8.jpg') no-repeat center center / cover; height: 300px"><i
                                    class="fa fa-play"></i></a>

                        </div>
                    </div>
                </div>
            </div>

            <div class="section nobg" id="details">
                <div class="container clearfix">
                    <div class="row justify-content-center mb-5">
                        <div class="col-md-10 center">
                            <div class="heading-block nobottomborder mb-4">
                                <h2 class="mb-4 nott" id="other_details_title">More To Know Us</h2>
                            </div>
                            <div class="svg-line bottommargin-sm clearfix">
                                <img src="/static/xsite_template/all_templates/xsite_template_four/images/divider-1.svg"
                                     alt="svg divider"
                                     height="20">
                            </div>
                            <p id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bgcolor subscribe-section position-relative" style="margin-top: 100px;" >
                <div class="container" style="z-index: 2;">
                    <div class="center collapsed subscribe-section-target" data-toggle="collapse"
                         data-target="#target-1">
                        <div class="subscribe-icon"><i class="fa fa-envelope"></i></div>
                        <h2 class="mb-0 mt-2 position-relative" style="z-index: 1;" id="banner_title1">Find Your Dream Home Here! Beautiful Homes At Ugly Home Prices.
                            <i class="fa fa-arrow-down position-relative" style="top: 5px"></i>
                        </h2>
                    </div>
                    <div class="collapse show" id="target-1">
                        <div class="form-widget pb-5" data-alert-type="false">

                            <div class="form-result"></div>

                            <div class="nonprofit-loader css3-spinner" style="position: absolute;">
                                <div class="css3-spinner-bounce1"></div>
                                <div class="css3-spinner-bounce2"></div>
                                <div class="css3-spinner-bounce3"></div>
                            </div>
                            <div id="nonprofit-submitted" class="center">
                                <h4 class="t600 mb-0">Thank You for Contact Us! Our Team will contact you asap on your
                                    email Address.</h4>
                            </div>
                                <form id="buyer_form" class="row mt-2" method="post">
                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-name-buyer">Name <small>*</small></label>
                                        <input type="text"
                                               name="fullname"
                                               id="template-contactform-name-buyer"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Full Name">
                                    </div>

                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-email-buyer">Email <small>*</small></label>
                                        <input type="email" name="email"
                                               id="template-contactform-email-buyer"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Email"/>
                                    </div>

                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-phone-buyer">Phone<small>*</small></label>
                                        <input type="text" name="phone" id="template-contactform-phone-buyer"
                                               class="form-control border-form-control"
                                               placeholder="Enter your Contact Number">
                                    </div>
                                    <div class="col-md-3 mb-4 mb-md-1">
                                        <label for="template-contactform-service-buyer">What are you looking
                                            for?</label>
                                        <select id="template-contactform-service-buyer"
                                                name="what_are_you_looking_for"
                                                class="form-control border-form-control">
                                            <option value="">What are you looking for?</option>
                                        </select>

                                    </div>
                                    <input type="hidden" name="audience" value="Buyer">
                                    <button class="btn button button-rounded button-xlarge button-dark bg-dark shadow nott ls0 m-0 subscribe-button"
                                            type="submit"
                                            name="template-contactform-submit"
                                            id="template-contactform-submit-buyer"
                                            value="submit"> Get your book
                                    </button>

                                </form>
                                <form id="seller_form" class="row mt-2" method="post">
                                    <div class="col-md-4 mb-4 mb-md-1">
                                        <label for="template-contactform-name-seller">Name <small>*</small></label>
                                        <input type="text"
                                               name="fullname"
                                               id="template-contactform-name-seller"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Full Name">
                                    </div>

                                    <div class="col-md-4 mb-4 mb-md-1">
                                        <label for="template-contactform-email-seller">Email <small>*</small></label>
                                        <input type="email"
                                               name="email"
                                               id="template-contactform-email-seller"
                                               class="form-control border-form-control required"
                                               placeholder="Enter your Email"/>
                                    </div>

                                    <div class="col-md-4 mb-4 mb-md-1">
                                        <label for="template-contactform-phone-seller">Phone<small>*</small></label>
                                        <input type="text" name="phone" id="template-contactform-phone-seller"
                                               class="form-control border-form-control"
                                               placeholder="Enter your Contact Number">
                                    </div>
                                    <div class="col-md-12 mb-4 mb-md-3 mt-3 text-center">
                                        <div class="form-check">
                                            <label class="form-check-label">

                                                <input name="immediate_assistance" id="immediate_assistance"
                                                       type="checkbox"
                                                       class="form-check-input" onclick="javascript:ShowFields()">
                                                I
                                                would like
                                                immediate assistance
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-md-12 mb-4 mb-md-1">
                                        <div id="immediate_assistance_fields" style="display: none">
                                            <div class="row">
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-address-seller">Street
                                                        Address</label>
                                                    <input type="text" id="template-contactform-address-seller"
                                                           name="street_address"
                                                           class="form-control border-form-control required"
                                                           placeholder="Enter Your Street Address.."/>
                                                </div>

                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-city-seller">City</label>
                                                    <input type="text" id="template-contactform-city-seller"
                                                           name="city"
                                                           class="form-control border-form-control required"
                                                           placeholder="Enter Your City.."/>
                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-state-seller">State</label>
                                                    <select id="template-contactform-state-seller" name="state"
                                                            class="form-control border-form-control">
                                                        <option value="">State</option>
                                                        <option value="AL">
                                                            Alabama
                                                        </option>
                                                        <option value="AK">
                                                            Alaska
                                                        </option>
                                                        <option value="AB">
                                                            Alberta
                                                        </option>
                                                        <option value="AS">
                                                            American Samoa
                                                        </option>
                                                        <option value="AZ">
                                                            Arizona
                                                        </option>
                                                        <option value="AR">
                                                            Arkansas
                                                        </option>
                                                        <option value="BC">
                                                            British Columbia
                                                        </option>
                                                        <option value="CA">
                                                            California
                                                        </option>
                                                        <option value="CO">
                                                            Colorado
                                                        </option>
                                                        <option value="CT">
                                                            Connecticut
                                                        </option>
                                                        <option value="DE">
                                                            Delaware
                                                        </option>
                                                        <option value="FM">
                                                            Fed. St. of Micronesia
                                                        </option>
                                                        <option value="FL">
                                                            Florida
                                                        </option>
                                                        <option value="GA">
                                                            Georgia
                                                        </option>
                                                        <option value="GU">
                                                            Guam
                                                        </option>
                                                        <option value="HI">
                                                            Hawaii
                                                        </option>
                                                        <option value="ID">
                                                            Idaho
                                                        </option>
                                                        <option value="IL">
                                                            Illinois
                                                        </option>
                                                        <option value="IN">
                                                            Indiana
                                                        </option>
                                                        <option value="IA">
                                                            Iowa
                                                        </option>
                                                        <option value="KS">
                                                            Kansas
                                                        </option>
                                                        <option value="KY">
                                                            Kentucky
                                                        </option>
                                                        <option value="LA">
                                                            Louisiana
                                                        </option>
                                                        <option value="ME">
                                                            Maine
                                                        </option>
                                                        <option value="MB">
                                                            Manitoba
                                                        </option>
                                                        <option value="MH">
                                                            Marshall Islands
                                                        </option>
                                                        <option value="MD">
                                                            Maryland
                                                        </option>
                                                        <option value="MA">
                                                            Massachusetts
                                                        </option>
                                                        <option value="MI">
                                                            Michigan
                                                        </option>
                                                        <option value="MN">
                                                            Minnesota
                                                        </option>
                                                        <option value="MS">
                                                            Mississippi
                                                        </option>
                                                        <option value="MO">
                                                            Missouri
                                                        </option>
                                                        <option value="MT">
                                                            Montana
                                                        </option>
                                                        <option value="NE">
                                                            Nebraska
                                                        </option>
                                                        <option value="NV">
                                                            Nevada
                                                        </option>
                                                        <option value="NB">
                                                            New Brunswick
                                                        </option>
                                                        <option value="NH">
                                                            New Hampshire
                                                        </option>
                                                        <option value="NJ">
                                                            New Jersey
                                                        </option>
                                                        <option value="NM">
                                                            New Mexico
                                                        </option>
                                                        <option value="NY">
                                                            New York
                                                        </option>
                                                        <option value="NL">
                                                            Newfoundland
                                                        </option>
                                                        <option value="NC">
                                                            North Carolina
                                                        </option>
                                                        <option value="ND">
                                                            North Dakota
                                                        </option>
                                                        <option value="MP">
                                                            Northern Mariana Islands
                                                        </option>
                                                        <option value="NT">
                                                            Northwest Territory
                                                        </option>
                                                        <option value="NS">
                                                            Nova Scotia
                                                        </option>
                                                        <option value="NU">
                                                            Nunavut
                                                        </option>
                                                        <option value="OH">
                                                            Ohio
                                                        </option>
                                                        <option value="OK">
                                                            Oklahoma
                                                        </option>
                                                        <option value="ON">
                                                            Ontario
                                                        </option>
                                                        <option value="OR">
                                                            Oregon
                                                        </option>
                                                        <option value="PA">
                                                            Pennsylvania
                                                        </option>
                                                        <option value="PE">
                                                            Prince Edward Island
                                                        </option>
                                                        <option value="PR">
                                                            Puerto Rico
                                                        </option>
                                                        <option value="QC">
                                                            Quebec
                                                        </option>
                                                        <option value="RI">
                                                            Rhode Island
                                                        </option>
                                                        <option value="SK">
                                                            Saskatchewan
                                                        </option>
                                                        <option value="SC">
                                                            South Carolina
                                                        </option>
                                                        <option value="SD">
                                                            South Dakota
                                                        </option>
                                                        <option value="TN">
                                                            Tennessee
                                                        </option>
                                                        <option value="TX">
                                                            Texas
                                                        </option>
                                                        <option value="UT">
                                                            Utah
                                                        </option>
                                                        <option value="VT">
                                                            Vermont
                                                        </option>
                                                        <option value="VI">
                                                            Virgin Islands
                                                        </option>
                                                        <option value="VA">
                                                            Virginia
                                                        </option>
                                                        <option value="WA">
                                                            Washington
                                                        </option>
                                                        <option value="DC">
                                                            Washington DC
                                                        </option>
                                                        <option value="WV">
                                                                West Virginia
                                                        </option>
                                                        <option value="WI">
                                                            Wisconsin
                                                        </option>
                                                        <option value="WY">
                                                            Wyoming
                                                        </option>
                                                        <option value="YT">
                                                            Yukon Territory
                                                        </option>
                                                    </select>
                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-zip-seller">Zip/Postal Code</label>
                                                    <input type="text" id="template-contactform-zip-seller"
                                                           name="zip" placeholder="Enter Your Zip.."
                                                           class="form-control border-form-control required"/>

                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-is_home_listed-seller"> Is home
                                                        listed?</label>
                                                    <select id="template-contactform-is_home_listed-seller"
                                                            name="is_home_listed"
                                                            class="form-control border-form-control">
                                                        <option value="">Is home listed?</option>
                                                    </select>
                                                </div>
                                                <div class="col-md-4 mb-4 mb-md-3">
                                                    <label for="template-contactform-asking_price-seller">Asking
                                                        Price</label>
                                                    <input type="number" id="template-contactform-asking_price-seller"
                                                           name="asking_price" placeholder="Enter Your Asking Price.."
                                                           class="form-control border-form-control required" min="0"/>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <button class="btn button button-rounded button-xlarge button-dark bg-dark shadow nott ls0 m-0 subscribe-button"
                                            type="submit"
                                            name="template-contactform-submit"
                                            id="template-contactform-seller"
                                            value="submit"> Get your book
                                    </button>

                                </form>
                        </div>
                    </div>
                </div>
                <div style="background-image: url('/static/xsite_template/all_templates/xsite_template_four/images/divider-4.svg'); position: absolute; bottom: -20px; left: 0; width: 100%; height: 60px; z-index: 1;"></div>
            </div>

            <div class="line line-sm my-0 clearfix"></div>
            <div class="clear"></div>
            <div class="section section-details mb-0 bg-white" style="padding: 80px 0 80px;" id="testimonials">
                <div class="container clearfix">
                    <div class="row">
                        <div class="col-md-4 px-4 mb-2">
                            <h4 class="t500 mb-4">Contact Us</h4>
                            <abbr title="Phone Number"><strong>Phone:</strong></abbr> <span id="phone">03334455667</span><br>
                            <abbr title="Email Address"><strong>Email:</strong></abbr> <span id="email">support@gmail.com</span>
                        </div>
                        <div class="col-md-6 px-4 mb-5 mb-md-0">
                            <h4 class="t500 mb-3">Testimonials</h4>
                            <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget"
                                 data-margin="0" data-nav="false" data-pagi="false" data-items="1" data-autoplay="6000"
                                 data-loop="true" data-animate-in="fadeIn" data-animate-out="fadeOut">

                                <div class="oc-item">
                                    <div class="testimonial nobg noshadow noborder p-0">
                                        <div class="testi-content">
                                            <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                            <div class="testi-meta ls1" id="testi_1_person_name"> Person 1</div>
                                        </div>
                                    </div>
                                </div>
                                    <div class="oc-item">
                                        <div class="testimonial nobg noshadow noborder p-0">
                                            <div class="testi-content">
                                                <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                <div class="testi-meta ls1" id="testi_2_person_name"> Person 2</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="oc-item">
                                        <div class="testimonial nobg noshadow noborder p-0">
                                            <div class="testi-content">
                                                <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                <div class="testi-meta ls1" id="testi_3_person_name"> Person 3</div>
                                            </div>
                                        </div>
                                    </div>

                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer">


        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="bgcolor pb-2 pt-2">

            <div class="container clearfix">

                <div class="row justify-content-between align-items-center">
                    <div class="col-md-12 text-center">
                        &copy; 2020 <a class="text-dark" target="_blank" href="https://prospectx.com/">Prospectx</a>
                        All Rights Reserved.
                    </div>

                </div>

            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->

</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>
<script src="/static/xsite_template/js/jquery.calendario.js"></script>
<script src="/static/xsite_template/all_templates/xsite_template_four/js/events.js"></script>

<script>
    jQuery(document).ready(function ($) {
        $(".carousel-widget").owlCarousel({
            loop: true,
            items: 1
        });
        var elementParent = $('.floating-contact-wrap');
        $('.floating-contact-btn').off('click').on('click', function () {
            elementParent.toggleClass('active',);
        });
    });

</script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

 <script>
        $(document).ready(function () {
            $('#template-contactform-phone-buyer').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-phone-seller').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-zip-seller').focus(function () {
                var mask = "99999";
                $(this).inputmask(mask, {"placeholder": ""});
            });
        });
 </script>

</body>"""

    Dark_head = """<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta name="author" content="SemiColonWeb"/>
    <title>Xsite</title>

    <!-- Stylesheets
    ============================================= -->
    <link href="https://fonts.googleapis.com/css?family=Mukta+Vaani:300,400,500,600,700|Open+Sans:300,400,600,700,800,900"
          rel="stylesheet" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_five/car.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/swiper.css" type="text/css"/>

    <!-- Bootstrap Select CSS -->
    <link rel="stylesheet" href="/static/xsite_template/css/components/bs-select.css" type="text/css"/>

    <!-- car Specific Stylesheet -->
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_five/car.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_five/css/car-icons/style.css"
          type="text/css"/>
    <!-- / -->

    <link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_five/css/fonts.css"
          type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>

    <link rel="stylesheet" href="/static/xsite_template/css/colors.php?color=c85e51" type="text/css"/>
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">

    <!-- Document Title
    ============================================= -->
    <style>
        /* Revolution Slider */
        .ares .tp-tab {
            border: 1px solid #eee;
        }

        .ares .tp-tab-content {
            margin-top: -4px;
        }

        .ares .tp-tab-content {
            padding: 15px 15px 15px 110px;
        }

        .ares .tp-tab-image {
            width: 80px;
            height: 80px;
        }

    </style>

</head>"""
    Dark_body = """<body class="stretched side-push-panel"
      data-loader-html="<div><img src='demos/car/images/page-loader.gif' alt='Loader'></div>">

<!-- Side Panel Overlay -->
<div class="body-overlay"></div>


<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">
    <!-- Header
    ============================================= -->
    <header id="header" class="static-sticky full-header clearfix">

        <div id="header-wrap">

            <div class="container-fluid clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                    ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo"><img
                            src="/media/xsite_images/website_logos/prospectx-logo.png"
                            alt="Canvas Logo"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu" class="with-arrows clearfix">
                    <ul>
                        <li class="current"><a href="#">
                            <div>Home</div>
                        </a></li>
                        <!-- Mega Menu -->

                        <li><a href="#about">
                            <div>About</div>
                        </a></li>
                        <li><a href="#details">
                            <div>Details</div>
                        </a></li>
                        <li><a href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                    </ul>
                </nav><!-- #primary-menu end -->
            </div>

        </div>

        <div id="header-trigger"><i class="icon-line-menu"></i><i class="icon-line-cross"></i></div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element swiper_wrapper full-screen force-full-screen clearfix" data-dots="true"
             data-loop="true" data-grab="false">

        <div class="swiper-container swiper-parent">
            <div class="swiper-wrapper">
                <div class="swiper-slide dark"
                     style="background-image: url('/static/xsite_template/all_templates/xsite_template_five/images/hero-slider/3.jpg'); background-size: cover">
                    <div class="container clearfix">
                        <div class="slider-caption slider-caption-center">
                            <h2 class="font-primary nott" id="banner_title">Find Your Dream Home Here! Beautiful Homes
                                At Ugly Home Prices.</h2>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </section><!-- #Slider End -->

    <!-- Content
    ============================================= -->
    <section id="content" class="clearfix">

        <div class="content-wrap nobottompadding" style="padding-top: 1px">

            <!-- Masonry Thums
            ============================================= -->


            <!-- Moving car on scroll
            ============================================= -->
            <div class="section notopmargin clearfix" style="padding: 100px 0" id="about">
                <div class="running-car topmargin-sm">
                    <img class="car"
                         src="/static/xsite_template/all_templates/xsite_template_five/images/moving-car/car.jpg"
                         alt="">
                    <img class="wheel"
                         src="/static/xsite_template/all_templates/xsite_template_five/images/moving-car/car-tier.png"
                         alt="">
                </div>
                <div class="container clearfix">
                    <div class="row clearfix" style="position: relative;">
                        <div class="col-lg-6 offset-lg-6">
                            <div class="heading-block hlarge">
                                <h3 id="about_us_title">Little More Detail About Us</h3>
                            </div>
                            <p id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                accusantium
                                doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et
                                quasi
                                architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas
                                sit
                                aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                                voluptatem
                                sequi nesciunt?</p>
                        </div>
                    </div>
                </div>
            </div> <!-- Moving car on scroll End -->

            <!-- 360 degree car
            ============================================= -->
            <div class="section dark nobottommargin clearfix" id="details"
                 style="background: #FFF url('/static/xsite_template/all_templates/xsite_template_five/images/1.jpg') right bottom no-repeat; background-size: cover; padding: 80px 0 20px">
                <div class="container-fluid clearfix" style="position: relative; z-index: 2;">
                    <div class="row clearfix">
                        <div class="col-lg-8">
                            <div class="heading-block noborder nobottommargin center">
                                <h3 style="font-size: 32px;  font-weight: 700;">360 Degree Drag</h3>
                            </div>
                            <!-- 360 degree Car Content -->
                            <div class="threesixty 360-car">
                                <div class="spinner">
                                    <span>0%</span>
                                </div>
                                <ol class="threesixty_images"></ol>
                            </div>

                        </div>
                        <div class="col-lg-4">
                            <div class="row clearfix">
                                <div class="col-lg-10 mt-3">
                                    <form id="buyer_form" name="quick-contact-form"
                                          class="quick-contact-form nobottommargin" method="post">
                                        <div class="form-process"></div>
                                        <input type="text"
                                               name="fullname"
                                               id="template-contactform-name-buyer" placeholder="Name"
                                               class="required border-form-control sm-form-control input-block-level"/>
                                        <input type="email"
                                               name="email"
                                               id="template-contactform-email-buyer" placeholder="Email"
                                               class="required border-form-control sm-form-control email input-block-level"/>
                                        <input type="text" id="template-contactform-phone-buyer"
                                               name="phone" placeholder="Phone"
                                               class="required border-form-control sm-form-control input-block-level"/>
                                        <select id="template-contactform-service-buyer"
                                                name="what_are_you_looking_for"
                                                class="required border-form-control sm-form-control input-block-level">
                                            <option value="">What are you looking for?</option>
                                        </select>

                                        <input type="hidden" name="audience" value="Buyer"/>
                                        <div class="col_full nobottommargin">
                                            <button class="button button-rounded btn-block t400 nomargin"
                                                    type="submit" id="template-contactform-submit-buyer"
                                                    name="template-contactform-submit"
                                                    value="submit">Get your ebook
                                            </button>
                                        </div>

                                    </form>
                                    <form id="seller_form" name="quick-contact-form"
                                          class="quick-contact-form nobottommargin" method="post">
                                        <div class="form-process"></div>
                                        <input type="hidden" name="audience" value="Seller"/>
                                        <input type="text" id="template-contactform-name-seller"
                                               name="fullname" placeholder="Name"
                                               class="required border-form-control sm-form-control input-block-level"/>
                                        <input type="text" id="template-contactform-phone-seller"
                                               name="phone" placeholder="Phone"
                                               class="required border-form-control sm-form-control input-block-level"/>
                                        <input type="email" id="template-contactform-email-seller"
                                               name="email" placeholder="Email"
                                               class="required border-form-control sm-form-control email input-block-level"/>

                                        <div class="form-check">
                                            <label class="form-check-label">

                                                <input name="immediate_assistance" id="immediate_assistance"
                                                       type="checkbox"
                                                       class="form-check-input"
                                                       onclick="javascript:ShowFields()">
                                                I
                                                would like
                                                immediate assistance
                                            </label>
                                        </div>

                                        <div id="immediate_assistance_fields" style="display: none">
                                            <input type="text" id="template-contactform-address-seller"
                                                   name="street_address" placeholder="Street Address"
                                                   class="required border-form-control sm-form-control input-block-level"/>
                                            <input type="text" id="template-contactform-city-seller"
                                                   name="city" placeholder="City"
                                                   class="required border-form-control sm-form-control input-block-level"/>
                                            <select id="template-contactform-state-seller" name="state"
                                                    class="required border-form-control sm-form-control input-block-level">
                                                <option value="">State</option>
                                                <option value="AL">
                                                    Alabama
                                                </option>
                                                <option value="AK">
                                                    Alaska
                                                </option>
                                                <option value="AB">
                                                    Alberta
                                                </option>
                                                <option value="AS">
                                                    American Samoa
                                                </option>
                                                <option value="AZ">
                                                    Arizona
                                                </option>
                                                <option value="AR">
                                                    Arkansas
                                                </option>
                                                <option value="BC">
                                                    British Columbia
                                                </option>
                                                <option value="CA">
                                                    California
                                                </option>
                                                <option value="CO">
                                                    Colorado
                                                </option>
                                                <option value="CT">
                                                    Connecticut
                                                </option>
                                                <option value="DE">
                                                    Delaware
                                                </option>
                                                <option value="FM">
                                                    Fed. St. of Micronesia
                                                </option>
                                                <option value="FL">
                                                    Florida
                                                </option>
                                                <option value="GA">
                                                    Georgia
                                                </option>
                                                <option value="GU">
                                                    Guam
                                                </option>
                                                <option value="HI">
                                                    Hawaii
                                                </option>
                                                <option value="ID">
                                                    Idaho
                                                </option>
                                                <option value="IL">
                                                    Illinois
                                                </option>
                                                <option value="IN">
                                                    Indiana
                                                </option>
                                                <option value="IA">
                                                    Iowa
                                                </option>
                                                <option value="KS">
                                                    Kansas
                                                </option>
                                                <option value="KY">
                                                    Kentucky
                                                </option>
                                                <option value="LA">
                                                    Louisiana
                                                </option>
                                                <option value="ME">
                                                    Maine
                                                </option>
                                                <option value="MB">
                                                    Manitoba
                                                </option>
                                                <option value="MH">
                                                    Marshall Islands
                                                </option>
                                                <option value="MD">
                                                    Maryland
                                                </option>
                                                <option value="MA">
                                                    Massachusetts
                                                </option>
                                                <option value="MI">
                                                    Michigan
                                                </option>
                                                <option value="MN">
                                                    Minnesota
                                                </option>
                                                <option value="MS">
                                                    Mississippi
                                                </option>
                                                <option value="MO">
                                                    Missouri
                                                </option>
                                                <option value="MT">
                                                    Montana
                                                </option>
                                                <option value="NE">
                                                    Nebraska
                                                </option>
                                                <option value="NV">
                                                    Nevada
                                                </option>
                                                <option value="NB">
                                                    New Brunswick
                                                </option>
                                                <option value="NH">
                                                    New Hampshire
                                                </option>
                                                <option value="NJ">
                                                    New Jersey
                                                </option>
                                                <option value="NM">
                                                    New Mexico
                                                </option>
                                                <option value="NY">
                                                    New York
                                                </option>
                                                <option value="NL">
                                                    Newfoundland
                                                </option>
                                                <option value="NC">
                                                    North Carolina
                                                </option>
                                                <option value="ND">
                                                    North Dakota
                                                </option>
                                                <option value="MP">
                                                    Northern Mariana Islands
                                                </option>
                                                <option value="NT">
                                                    Northwest Territory
                                                </option>
                                                <option value="NS">
                                                    Nova Scotia
                                                </option>
                                                <option value="NU">
                                                    Nunavut
                                                </option>
                                                <option value="OH">
                                                    Ohio
                                                </option>
                                                <option value="OK">
                                                    Oklahoma
                                                </option>
                                                <option value="ON">
                                                    Ontario
                                                </option>
                                                <option value="OR">
                                                    Oregon
                                                </option>
                                                <option value="PA">
                                                    Pennsylvania
                                                </option>
                                                <option value="PE">
                                                    Prince Edward Island
                                                </option>
                                                <option value="PR">
                                                    Puerto Rico
                                                </option>
                                                <option value="QC">
                                                    Quebec
                                                </option>
                                                <option value="RI">
                                                    Rhode Island
                                                </option>
                                                <option value="SK">
                                                    Saskatchewan
                                                </option>
                                                <option value="SC">
                                                    South Carolina
                                                </option>
                                                <option value="SD">
                                                    South Dakota
                                                </option>
                                                <option value="TN">
                                                    Tennessee
                                                </option>
                                                <option value="TX">
                                                    Texas
                                                </option>
                                                <option value="UT">
                                                    Utah
                                                </option>
                                                <option value="VT">
                                                    Vermont
                                                </option>
                                                <option value="VI">
                                                    Virgin Islands
                                                </option>
                                                <option value="VA">
                                                    Virginia
                                                </option>
                                                <option value="WA">
                                                    Washington
                                                </option>
                                                <option value="DC">
                                                    Washington DC
                                                </option>
                                                <option value="WV">
                                                    West Virginia
                                                </option>
                                                <option value="WI">
                                                    Wisconsin
                                                </option>
                                                <option value="WY">
                                                    Wyoming
                                                </option>
                                                <option value="YT">
                                                    Yukon Territory
                                                </option>
                                            </select>

                                            <input type="text" id="template-contactform-zip-seller"
                                                   name="zip" placeholder="Zip"
                                                   class="required border-form-control sm-form-control input-block-level"/>
                                            <select id="template-contactform-is_home_listed-seller"
                                                    name="is_home_listed"
                                                    class="required border-form-control sm-form-control input-block-level">
                                                <option value="">Is home listed?</option>
                                            </select>
                                            <input type="number" id="template-contactform-asking_price-seller"
                                                   name="asking_price" placeholder="Asking Price"
                                                   class="required border-form-control sm-form-control input-block-level"
                                                   min="0"/>
                                        </div>

                                        <div class="col_full nobottommargin">
                                            <button class="button button-rounded btn-block t400 nomargin"
                                                    type="submit" id="template-contactform-seller"
                                                    name="template-contactform-submit"
                                                    value="submit">Get your ebook
                                            </button>
                                        </div>

                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="video-wrap d-block d-md-block d-lg-none" style="z-index: 0;">
                    <div class="video-overlay" style="background: rgba(255,255,255,0.0);"></div>
                </div>
            </div> <!-- 360 Degree Section End -->

            <!-- 360 degree car
            ============================================= -->
            <!-- Filter Car lists end -->

            <!-- Video Gallery on Hover
            ============================================= -->
            <!-- Video Gallery end -->

            <!-- Counter Area
            ============================================= -->

            <!-- Counter Area end -->

            <!-- Featured Section
            ============================================= -->
            <div class="section nomargin clearfix"
                 style="background: #FFF url('/static/xsite_template/all_templates/xsite_template_five/images/features/section-bg.jpg') left bottom no-repeat; background-size: cover; padding: 140px 0">
                <div class="container clearfix">
                    <div class="row clearfix">
                        <div class="col-lg-5 col-md-9">
                            <div class="heading-block">
                                <h3 style="font-size: 58px; line-height: 56px; letter-spacing: -2px"
                                    id="other_details_title">More To Know Us</h3>
                            </div>
                            <p id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                                veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam
                                voluptatem quia
                                voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui
                                ratione
                                voluptatem sequi nesciunt?</p>

                        </div>
                    </div>
                </div>
            </div> <!-- Featured end -->

            <!-- Buy And Sell Section
            ============================================= -->
            <div class="section nomargin nopadding clearfix" style="padding: 100px 0" id="testimonials">
                <div class="row align-items-stretch clearfix">


                    <div class=" offset-lg-3 col-md-8 col-lg-6 mb-4 mt-4">
                        <!-- <h3 class="mb-3 text-center">Testimonials</h3> -->
                        <h2 class="font-primary nott text-center">Testimonials</h2>
                        <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget text-center"
                             data-margin="0" data-items="1" data-loop="true" data-autoplay="5500" data-pagi="false">

                            <div class="oc-item">
                                <div class="testimonial noborder noshadow ">

                                    <div class="testi-content border-bottom pb-4">
                                        <p id="testi_1_text">Sed ut perspiciatis unde omnis
                                            iste natus error sit voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="mt-2">
                                            <i class="fa fa-star"></i> <i class="fa fa-star"></i> <i
                                                class="fa fa-star"></i> <i class="fa fa-star"></i> <i
                                                class="far fa-star"></i>
                                        </div>
                                        <div class="testi-meta"><span id="testi_1_person_name">Person 1</span><span
                                                id="testi_1_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="oc-item">
                                <div class="testimonial noborder noshadow">

                                    <div class="testi-content border-bottom pb-4">
                                        <p id="testi_2_text">Sed ut perspiciatis unde omnis
                                            iste natus error sit voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="mt-2">
                                            <i class="fa fa-star"></i> <i class="fa fa-star"></i> <i
                                                class="fa fa-star"></i> <i class="fa fa-star"></i> <i
                                                class="fa fa-star-half"></i>
                                        </div>
                                        <div class="testi-meta">
                                            <span id="testi_2_person_name">Person 2</span>
                                            <span id="testi_2_company_name">Argon Tech 2</span>
                                        </div>
                                    </div>
                                </div>

                            </div>
                            <div class="oc-item">
                                <div class="testimonial noborder noshadow">

                                    <div class="testi-content border-bottom pb-4">
                                        <p id="testi_3_text">Sed ut perspiciatis unde omnis
                                            iste natus error sit voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="mt-2">
                                            <i class="fa fa-star"></i> <i class="fa fa-star"></i> <i
                                                class="fa fa-star"></i> <i class="fa fa-star"></i> <i
                                                class="fa fa-star"></i>
                                        </div>
                                        <div class="testi-meta">
                                            <span id="testi_3_person_name">Person 3</span>
                                            <span id="testi_3_company_name">Argon Tech 3</span>
                                        </div>
                                    </div>
                                </div>

                            </div>

                        </div>
                    </div>
                </div>
            </div>


        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="dark noborder" style="background-color: #080808;">

        <div class="container-fluid clearfix">


            <div class="footer-widgets-wrap clearfix pt-2 pb-2" style="padding: 30px;">

                <div class="row ">


                    <div class="col-lg-12 fright tright   col_last">


                        <div style="color: #fff">
                            <span> &copy; 2020 <a class="footer_copyright" target="_blank"
                                                  href="https://prospectx.com/">Prospectx</a>
                    All Rights Reserved.</span>
                            <div class="clear"></div>
                        </div>

                    </div>
                </div>

            </div>

        </div>

    </footer>


</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- Contact Button
============================================= -->
<!-- <div id="contact-me" class="fa fa-envelope side-panel-trigger bgcolor"></div> -->

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>
<script src="/static/xsite_template/all_templates/xsite_template_five/js/360rotator.js"></script>

<!-- Bootstrap Select Plugin -->
<script src="/static/xsite_template/js/components/bs-select.js"></script>

<!-- SLIDER REVOLUTION 5.x SCRIPTS  -->

<script>

    //Car Appear In View
    function isScrolledIntoView(elem) {
        var docViewTop = $(window).scrollTop();
        var docViewBottom = docViewTop + $(window).height();

        var elemTop = $(elem).offset().top + 180;
        var elemBottom = elemTop + $(elem).height() - 500;

        return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
    }

    $(window).scroll(function () {
        $('.running-car').each(function () {
            if (isScrolledIntoView(this) === true) {
                $(this).addClass('in-view');
            } else {
                $(this).removeClass('in-view');
            }
        });
    });

    //threesixty degree
    window.onload = init;
    var car;

    function init() {

        car = $('.360-car').ThreeSixty({
            totalFrames: 52, // Total no. of image you have for 360 slider
            endFrame: 52, // end frame for the auto spin animation
            currentFrame: 3, // This the start frame for auto spin
            imgList: '.threesixty_images', // selector for image list
            progress: '.spinner', // selector to show the loading progress
            imagePath: '/static/xsite_template/all_templates/xsite_template_five/images/360degree-cars/', // path of the image assets
            filePrefix: '', // file prefix if any
            ext: '.png', // extention for the assets
            height: 887,
            width: 500,
            navigation: true,
            responsive: true,
        });
    };

    // Rev Slider
    var tpj = jQuery;
    var revapi424;
    tpj(document).ready(function () {
        if (tpj("#rev_slider_424_1").revolution === undefined) {
            revslider_showDoubleJqueryError("#rev_slider_424_1");
        } else {
            revapi424 = tpj("#rev_slider_424_1").show().revolution({
                sliderType: "carousel",
                jsFileLocation: "include/rs-plugin/js/",
                sliderLayout: "auto",
                dottedOverlay: "none",
                delay: 7000,
                navigation: {
                    keyboardNavigation: "off",
                    keyboard_direction: "horizontal",
                    mouseScrollNavigation: "off",
                    mouseScrollReverse: "default",
                    onHoverStop: "off",
                    touch: {
                        touchenabled: "on",
                        swipe_threshold: 75,
                        swipe_min_touches: 1,
                        swipe_direction: "horizontal",
                        drag_block_vertical: false
                    }
                    ,
                    arrows: {
                        style: "uranus",
                        enable: false,
                        hide_onmobile: false,
                        hide_onleave: true,
                        hide_delay: 200,
                        hide_delay_mobile: 1200,
                        tmp: '',
                        left: {
                            h_align: "left",
                            v_align: "center",
                            h_offset: -10,
                            v_offset: 0
                        },
                        right: {
                            h_align: "right",
                            v_align: "center",
                            h_offset: -10,
                            v_offset: 0
                        }
                    },
                    carousel: {
                        maxRotation: 65,
                        vary_rotation: "on",
                        minScale: 55,
                        vary_scale: "on",
                        horizontal_align: "center",
                        vertical_align: "center",
                        fadeout: "on",
                        vary_fade: "on",
                        maxVisibleItems: 5,
                        infinity: "off",
                        space: 0,
                        stretch: "on"
                    }
                    ,
                    tabs: {
                        style: "ares",
                        enable: true,
                        width: 270,
                        height: 80,
                        min_width: 270,
                        wrapper_padding: 10,
                        wrapper_color: "transparent",
                        wrapper_opacity: "0.5",
                        tmp: '<div class="tp-tab-content">  <span class="tp-tab-date">{{param1}}</span>  <span class="tp-tab-title">{{title}}</span></div><div class="tp-tab-image"></div>',
                        visibleAmount: 7,
                        hide_onmobile: false,
                        hide_under: 420,
                        hide_onleave: false,
                        hide_delay_mobile: 1200,
                        hide_delay: 200,
                        direction: "horizontal",
                        span: true,
                        position: "outer-bottom",
                        space: 20,
                        h_align: "left",
                        v_align: "bottom",
                        h_offset: 0,
                        v_offset: 0
                    }
                },
                visibilityLevels: [1240, 1024, 778, 480],
                gridwidth: [1240, 992, 768, 420],
                gridheight: [600, 500, 960, 720],
                lazyType: "single",
                shadow: 0,
                spinner: "off",
                stopLoop: "off",
                stopAfterLoops: 0,
                stopAtSlide: 1,
                shuffle: "off",
                autoHeight: "off",
                hideThumbsOnMobile: "off",
                hideSliderAtLimit: 0,
                hideCaptionAtLimit: 0,
                hideAllCaptionAtLilmit: 0,
                debugMode: false,
                fallbacks: {
                    simplifyAll: "off",
                    nextSlideOnWindowFocus: "off",
                    disableFocusListener: false,
                }
            });
        }
    });	/*ready*/
</script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

 <script>
        $(document).ready(function () {
            $('#template-contactform-phone-buyer').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-phone-seller').focus(function () {
                var mask = "999-999-9999";
                $(this).inputmask(mask, {"placeholder": ""});
            });

            $('#template-contactform-zip-seller').focus(function () {
                var mask = "99999";
                $(this).inputmask(mask, {"placeholder": ""});
            });
        });
 </script>
</body>"""

    Business_head = """<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta name="author" content="SemiColonWeb"/>
    <title>Xsite</title>

    <!-- Stylesheets
    ============================================= -->
    <link href="http://fonts.googleapis.com/css?family=Poppins:300,400,400i,600,700|Open+Sans:300,400,600,700,800,900"
          rel="stylesheet" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_six/business.css"
          type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/swiper.css" type="text/css"/>

    <!-- Business Demo Specific Stylesheet -->
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_six/business.css"
          type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_six/css/fonts.css"
          type="text/css"/>
    <!-- / -->
    <link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>

    <!-- Theme Color
    ============================================= -->
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_six/css/colors.css"
          type="text/css"/>
    <link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">

</head>"""
    Business_body = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <!-- Header
============================================= -->
    <header id="header" class="transparent-header dark full-header" data-sticky-class="not-dark"
            data-responsive-class="not-dark" data-sticky-offset="full">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                   <a href="#" class="standard-logo"><img class="logo_img" src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Xsite logo"></a>
                    <!-- <a href="index.html" class="retina-logo" data-dark-logo="images/prospectx-logo.png"><img
                            src="images/prospectx-logo.png" alt="Canvas Logo"></a> -->
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu" class="not-dark">

                    <ul>
                        <li class="active"><a href="#Home">
                            <div>Home</div>
                        </a></li>
                        <li><a href="#About">
                            <div>About</div>
                        </a></li>
                        <li><a href="#Testimonials">
                            <div>Testimonials</div>
                        </a></li>
                        <li><a href="#Details">
                            <div>Details</div>
                        </a></li>

                    </ul>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element swiper_wrapper full-screen clearfix" data-loop="true">

        <div class="slider-parallax-inner" id="Home">
            <div class="swiper-container swiper-parent">
                <div class="swiper-wrapper">
                    <div class="swiper-slide dark"
                         style="background-image: url('/static/xsite_template/all_templates/xsite_template_six/images/slider/1.jpg'); background-size: cover">
                        <div class="container clearfix">
                            <div class="slider-caption slider-caption-center">

                                <h3 class="font-primary nott" id="banner_title">Find Your Dream Home Here! Beautiful
                                    Homes At Ugly Home Prices.
                                </h3>
                                <a href="#Testimonials"
                                   class="button button-rounded button-large nott ls0 font-primary button_Qoute banner_button_text">Get
                                    Your Ebook</a>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        </div>
    </section>
    <!-- About Us
            ============================================= -->
    <section id="About">
        <div class="content-wrap nobottompadding" style="z-index: 1; padding: 65px 0px;">
            <div class="container topmargin about_topmargin clearfix">
                <div class="heading-block center noborder">
                    <h3 style="font-size: 46px; font-weight: 700; letter-spacing: -2px; line-height: 58px"
                        id="about_us_title">Little More Detail About Us
                    </h3>
                </div>
                <div class="center col-lg-10 offset-lg-1 col-sm-12 bottommargin">
                    <p class="text-rotater font-secondary" data-separator="," data-rotate="fadeInRight"
                       data-speed="3500" id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit
                        voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</p>
                </div>

            </div>

        </div>

    </section>


    <!-- Video Sections
            ============================================= -->
    <section id="vedio_section" style="background-color: #F0F0F0;">
        <div class="section nobg notopmargin clearfix" style="margin-bottom:  0px; padding: 0px 0px 78px;">
            <div class="container clearfix">

                <div class="row topmargin-lg clearfix">
                    <div class="col-lg-6 nopadding">
                        <!-- Youtube Video Link
                                ============================================= -->
                        <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe">
                            <img src="/static/xsite_template/all_templates/xsite_template_six/images/sections/video.jpg"
                                 alt="Youtube Video" class="image_fade"
                                 style="box-shadow: 0px 0px 25px 0px rgba(0,0,0,0.15); border-radius: 6px;">
                            <i class="fa fa-play"
                               style="position: absolute; top: 50%; left: 50%; font-size: 60px; color: #FFF; margin-top: -45px; margin-left: -23px"></i>
                        </a>
                    </div>
                    <!-- Video Texts
                            ============================================= -->
                    <div class="col-lg-6" style="padding-left: 22px;">
                        <div class="heading-block topmargin-sm bottommargin-sm noborder">
                            <h3 class="nott"
                                style="font-size: 46px; font-weight: 700; letter-spacing: -2px; line-height: 58px"
                                id="video_title">
                                Video </h3>
                        </div>
                        <p class="t400" id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                            accusantium
                            doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et
                            quasi
                            architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                            aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                            voluptatem
                            sequi nesciunt?

                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Parallax Area
            ============================================= -->
    <section id="terminals_form">
        <div id="Testimonials" class="section parallax topmargin-lg nobottommargin notopborder clearfix"
             style="padding-bottom: 65px;padding-top: 65px; background-color: #18181A; margin-top: 0px !important;">
            <div class="container clearfix">

                <div class="row cleafix mt-10">
                    <div class="col-lg-4">

                        <div class="card shadow-sm">
                            <div class="card-body">
                                <div class="card shadow-sm">
                                    <div class="card-body">
                                        <h4 class="mb-3">We give FAIR cash offers for your home! Fill out the form on to get an offer</h4>
                                        <form id="buyer_form" class="nobottommargin "
                                              name="template-contactform"
                                              method="post">
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-name-buyer">Name:<small>*</small></label>
                                                <input type="text"
                                                       name="fullname"
                                                       id="template-contactform-name-buyer"
                                                       class="form-control input-sm required">
                                            </div>

                                            <div class="col_full mb-3">
                                                <label for="template-contactform-email-buyer">Email
                                                    Address:<small>*</small></label>
                                                <input type="email"
                                                       name="email"
                                                       class="form-control input-sm required"
                                                       id="template-contactform-email-buyer">
                                            </div>
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-phone-buyer">Phone:<small>*</small></label>
                                                <input type="text" id="template-contactform-phone-buyer"
                                                       name="phone"
                                                       class="form-control input-sm required">

                                            </div>

                                            <div class="col_full mb-3">
                                                <label for="template-contactform-service-buyer">What are you
                                                    looking
                                                    for?</label>
                                                <select id="template-contactform-service-buyer"
                                                        name="what_are_you_looking_for"
                                                        class="form-control input-sm required">
                                                    <option value="">What are you looking for?</option>
                                                </select>

                                            </div>
                                            <input type="hidden" name="audience" value="Buyer">
                                            <div class="col_full nobottommargin">
                                                <button class="button button-rounded btn-block nott ls0 m-0"
                                                        type="submit"
                                                        name="template-contactform-submit"
                                                        id="template-contactform-submit-buyer"
                                                        value="submit"> Get Your Ebook
                                                </button>
                                            </div>

                                        </form>
                                        <form id="seller_form" class="nobottommargin "
                                              name="template-contactform"
                                              method="post">
                                            <input type="hidden" name="audience" value="Seller">
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-name-seller">Name:<small>*</small></label>
                                                <input type="text" id="template-contactform-name-seller"
                                                       name="fullname"
                                                       class="form-control input-sm required"/>
                                            </div>
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-phone-seller">Phone:<small>*</small></label>
                                                <input type="text" id="template-contactform-phone-seller"
                                                       name="phone"
                                                       class="form-control input-sm required"/>
                                            </div>
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-email-seller">Email
                                                    Address:<small>*</small></label>
                                                <input type="email" id="template-contactform-email-seller"
                                                       name="email"
                                                       class="form-control input-sm required"/>
                                            </div>

                                            <div class="col_full mb-3">

                                                <div class="form-check">
                                                    <label class="form-check-label">

                                                        <input name="immediate_assistance"
                                                               id="immediate_assistance"
                                                               type="checkbox"
                                                               class="form-check-input"
                                                               onclick="javascript:ShowFields()">

                                                        I
                                                        would like
                                                        immediate assistance
                                                    </label>
                                                </div>
                                            </div>

                                            <div id="immediate_assistance_fields" style="display: none">
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-address-seller">Street
                                                        Address:</label>
                                                    <input type="text"
                                                           id="template-contactform-address-seller"
                                                           name="street_address"
                                                           class="form-control input-sm required"/>
                                                </div>

                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-city-seller">City:</label>
                                                    <input type="text" id="template-contactform-city-seller"
                                                           name="city"
                                                           class="form-control input-sm required"/>
                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-state-seller">State:</label>
                                                    <select id="template-contactform-state-seller"
                                                            name="state"
                                                            class="form-control input-sm required">
                                                        <option value="">State</option>
                                                        <option value="AL">
                                                            Alabama
                                                        </option>
                                                        <option value="AK">
                                                            Alaska
                                                        </option>
                                                        <option value="AB">
                                                            Alberta
                                                        </option>
                                                        <option value="AS">
                                                            American Samoa
                                                        </option>
                                                        <option value="AZ">
                                                            Arizona
                                                        </option>
                                                        <option value="AR">
                                                            Arkansas
                                                        </option>
                                                        <option value="BC">
                                                            British Columbia
                                                        </option>
                                                        <option value="CA">
                                                            California
                                                        </option>
                                                        <option value="CO">
                                                            Colorado
                                                        </option>
                                                        <option value="CT">
                                                            Connecticut
                                                        </option>
                                                        <option value="DE">
                                                            Delaware
                                                        </option>
                                                        <option value="FM">
                                                            Fed. St. of Micronesia
                                                        </option>
                                                        <option value="FL">
                                                            Florida
                                                        </option>
                                                        <option value="GA">
                                                            Georgia
                                                        </option>
                                                        <option value="GU">
                                                            Guam
                                                        </option>
                                                        <option value="HI">
                                                            Hawaii
                                                        </option>
                                                        <option value="ID">
                                                            Idaho
                                                        </option>
                                                        <option value="IL">
                                                            Illinois
                                                        </option>
                                                        <option value="IN">
                                                            Indiana
                                                        </option>
                                                        <option value="IA">
                                                            Iowa
                                                        </option>
                                                        <option value="KS">
                                                            Kansas
                                                        </option>
                                                        <option value="KY">
                                                            Kentucky
                                                        </option>
                                                        <option value="LA">
                                                            Louisiana
                                                        </option>
                                                        <option value="ME">
                                                            Maine
                                                        </option>
                                                        <option value="MB">
                                                            Manitoba
                                                        </option>
                                                        <option value="MH">
                                                            Marshall Islands
                                                        </option>
                                                        <option value="MD">
                                                            Maryland
                                                        </option>
                                                        <option value="MA">
                                                            Massachusetts
                                                        </option>
                                                        <option value="MI">
                                                            Michigan
                                                        </option>
                                                        <option value="MN">
                                                            Minnesota
                                                        </option>
                                                        <option value="MS">
                                                            Mississippi
                                                        </option>
                                                        <option value="MO">
                                                            Missouri
                                                        </option>
                                                        <option value="MT">
                                                            Montana
                                                        </option>
                                                        <option value="NE">
                                                            Nebraska
                                                        </option>
                                                        <option value="NV">
                                                            Nevada
                                                        </option>
                                                        <option value="NB">
                                                            New Brunswick
                                                        </option>
                                                        <option value="NH">
                                                            New Hampshire
                                                        </option>
                                                        <option value="NJ">
                                                            New Jersey
                                                        </option>
                                                        <option value="NM">
                                                            New Mexico
                                                        </option>
                                                        <option value="NY">
                                                            New York
                                                        </option>
                                                        <option value="NL">
                                                            Newfoundland
                                                        </option>
                                                        <option value="NC">
                                                            North Carolina
                                                        </option>
                                                        <option value="ND">
                                                            North Dakota
                                                        </option>
                                                        <option value="MP">
                                                            Northern Mariana Islands
                                                        </option>
                                                        <option value="NT">
                                                            Northwest Territory
                                                        </option>
                                                        <option value="NS">
                                                            Nova Scotia
                                                        </option>
                                                        <option value="NU">
                                                            Nunavut
                                                        </option>
                                                        <option value="OH">
                                                            Ohio
                                                        </option>
                                                        <option value="OK">
                                                            Oklahoma
                                                        </option>
                                                        <option value="ON">
                                                            Ontario
                                                        </option>
                                                        <option value="OR">
                                                            Oregon
                                                        </option>
                                                        <option value="PA">
                                                            Pennsylvania
                                                        </option>
                                                        <option value="PE">
                                                            Prince Edward Island
                                                        </option>
                                                        <option value="PR">
                                                            Puerto Rico
                                                        </option>
                                                        <option value="QC">
                                                            Quebec
                                                        </option>
                                                        <option value="RI">
                                                            Rhode Island
                                                        </option>
                                                        <option value="SK">
                                                            Saskatchewan
                                                        </option>
                                                        <option value="SC">
                                                            South Carolina
                                                        </option>
                                                        <option value="SD">
                                                            South Dakota
                                                        </option>
                                                        <option value="TN">
                                                            Tennessee
                                                        </option>
                                                        <option value="TX">
                                                            Texas
                                                        </option>
                                                        <option value="UT">
                                                            Utah
                                                        </option>
                                                        <option value="VT">
                                                            Vermont
                                                        </option>
                                                        <option value="VI">
                                                            Virgin Islands
                                                        </option>
                                                        <option value="VA">
                                                            Virginia
                                                        </option>
                                                        <option value="WA">
                                                            Washington
                                                        </option>
                                                        <option value="DC">
                                                            Washington DC
                                                        </option>
                                                        <option value="WV">
                                                            West Virginia
                                                        </option>
                                                        <option value="WI">
                                                            Wisconsin
                                                        </option>
                                                        <option value="WY">
                                                            Wyoming
                                                        </option>
                                                        <option value="YT">
                                                            Yukon Territory
                                                        </option>
                                                    </select>
                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-zip-seller">Zip/Postal
                                                        Code:</label>
                                                    <input type="text" id="template-contactform-zip-seller"
                                                           name="zip"
                                                           class="form-control input-sm required"/>

                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-is_home_listed-seller">
                                                        Is
                                                        home
                                                        listed?</label>
                                                    <select id="template-contactform-is_home_listed-seller"
                                                            name="is_home_listed"
                                                            class="form-control input-sm required">
                                                        <option value="">Is home listed?</option>
                                                    </select>
                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-asking_price-seller">Asking
                                                        Price:</label>
                                                    <input type="number"
                                                           id="template-contactform-asking_price-seller"
                                                           name="asking_price"
                                                           class="form-control input-sm required" min="0"/>
                                                </div>
                                            </div>
                                            <div class="col_full nobottommargin">
                                                <button class="button button-rounded btn-block nott ls0 m-0"
                                                        type="submit"
                                                        name="template-contactform-submit"
                                                        id="template-contactform-seller"
                                                        value="submit"> GET your book
                                                </button>
                                            </div>

                                        </form>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>

                    <div class="topmargin d-block d-lg-none d-xl-block"></div>


                    <div class="col-lg-7 offset-lg-1 col-md-12 mt-4">
                        <h4 class="dark ">Testimonials</h4>
                        <div class="fslider testimonial" data-animation="slide" data-arrows="false">
                            <div id="testimonial_class" class="testimonial_class flexslider">
                                <div class="slider-wrap">
                                    <div class="slide">
                                        <div class="testimonial noborder noshadow">
                                            <div class="testi-content">
                                                <p class="bottommargin-sm font-primary" id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                <div class="testi-meta">
                                                    <span id="testi_1_person_name">Person 1</span>
                                                    <span  id="testi_1_company_name">Argon Tech 1</span>
                                                    <div class="testimonials-rating">
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                        <div class="slide">
                                            <div class="testimonial noborder noshadow">
                                                <div class="testi-content">
                                                    <p class="bottommargin-sm font-primary" id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                    <div class="testi-meta">
                                                         <span id="testi_2_person_name">Person 1</span>
                                                         <span  id="testi_2_company_name">Argon Tech 1</span>
                                                        <div class="testimonials-rating">
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="slide">
                                            <div class="testimonial noborder noshadow">
                                                <div class="testi-content">
                                                    <p class="bottommargin-sm font-primary" id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                    <div class="testi-meta">
                                                        <span id="testi_3_person_name">Person 1</span>
                                                        <span  id="testi_3_company_name">Argon Tech 1</span>
                                                        <div class="testimonials-rating">
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- Team Work
            ============================================= -->
    <div class="section nobg nobottompadding nobottommargin clearfix " id="Details"
         style="margin: 0; padding-top: 65px;">
        <div class="container clearfix">
            <div class="row clearfix">

                <div class="col-lg-6 order-lg-12">
                    <div class="device-xl device-md topmargin-lg"></div>
                    <h3 class="nobottommargin" style="font-size: 40px;" id="other_details_title">More To Know Us</h3>
                    <h3 class=" ls4 lowercase" style="font-size: 15px; color: #999;"></h3>
                    <p style="font-size: 20px;color: #888888; font-weight: 4;" id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
                    </p>
                </div>

                <div class="col-lg-6 order-lg-1">
                    <div style="position: relative; margin-bottom: 0;" class="ohidden" data-height-xl="520"
                         data-height-lg="520" data-height-md="520" data-height-sm="500" data-height-xs="300">
                        <img class="man ml-2"
                             src="/static/xsite_template/all_templates/xsite_template_six/images/sections/student_PNG62555.png"
                             style="position: absolute; top: 0; left: auto;" alt="Chrome">
                    </div>
                </div>

            </div>
        </div>
    </div>


</div>

</section>
<!-- #content end -->

<!-- Footer
    ============================================= -->
<footer id="#" class="noborder" style="padding: 30px 0; background-color: #000">

    <div class="container clearfix">
        <div class="col_two_third clearfix" style="margin: 0px;">
            <small class="t300" style="color: #fff">&copy; 2020 <strong><a class="text-dark"
                                                                           style="color: #fff !important"
                                                                           href="https://prospectx.com/"
                                                                           target="_blank">Prospectx</a></strong>
                All Rights Reserved.</small>
        </div>


    </div>

</footer>


</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script>
    // Owl Carousel Scripts
    $('#oc-features').owlCarousel({
        items: 1,
        margin: 60,
        nav: true,
        navText: ['<i class="fa fa-arrow-left"></i>', '<i class="fa fa-arrow-right"></i>'],
        dots: false,
        stagePadding: 30,
        responsive: {
            768: {items: 2},
            1200: {stagePadding: 200}
        },
    });
</script>
<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>
</body>"""

    Business_body_seller = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <!-- Header
============================================= -->
    <header id="header" class="transparent-header dark full-header" data-sticky-class="not-dark"
            data-responsive-class="not-dark" data-sticky-offset="full">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                   <a href="#" class="standard-logo"><img class="logo_img" src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Xsite logo"></a>
                    <!-- <a href="index.html" class="retina-logo" data-dark-logo="images/prospectx-logo.png"><img
                            src="images/prospectx-logo.png" alt="Canvas Logo"></a> -->
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu" class="not-dark">

                    <ul>
                        <li class="active"><a href="#Home">
                            <div>Home</div>
                        </a></li>
                        <li><a href="#About">
                            <div>About</div>
                        </a></li>
                        <li><a href="#Testimonials">
                            <div>Testimonials</div>
                        </a></li>
                        <li><a href="#Details">
                            <div>Details</div>
                        </a></li>

                    </ul>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element swiper_wrapper full-screen clearfix" data-loop="true">

        <div class="slider-parallax-inner" id="Home">
            <div class="swiper-container swiper-parent">
                <div class="swiper-wrapper">
                    <div class="swiper-slide dark"
                         style="background-image: url('/static/xsite_template/all_templates/xsite_template_six/images/slider/1.jpg'); background-size: cover">
                        <div class="container clearfix">
                            <div class="slider-caption slider-caption-center">

                                <h3 class="font-primary nott" id="banner_title">Find Your Dream Home Here! Beautiful
                                    Homes At Ugly Home Prices.
                                </h3>
                                <a href="#Testimonials"
                                   class="button button-rounded button-large nott ls0 font-primary button_Qoute banner_button_text">Get
                                    Your Ebook</a>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        </div>
    </section>
    <!-- About Us
            ============================================= -->
    <section id="About">
        <div class="content-wrap nobottompadding" style="z-index: 1; padding: 65px 0px;">
            <div class="container topmargin about_topmargin clearfix">
                <div class="heading-block center noborder">
                    <h3 style="font-size: 46px; font-weight: 700; letter-spacing: -2px; line-height: 58px"
                        id="about_us_title">Little More Detail About Us
                    </h3>
                </div>
                <div class="center col-lg-10 offset-lg-1 col-sm-12 bottommargin">
                    <p class="text-rotater font-secondary" data-separator="," data-rotate="fadeInRight"
                       data-speed="3500" id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit
                        voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</p>
                </div>

            </div>

        </div>

    </section>


    <!-- Video Sections
            ============================================= -->
    <section id="vedio_section" style="background-color: #F0F0F0;">
        <div class="section nobg notopmargin clearfix" style="margin-bottom:  0px; padding: 0px 0px 78px;">
            <div class="container clearfix">

                <div class="row topmargin-lg clearfix">
                    <div class="col-lg-6 nopadding">
                        <!-- Youtube Video Link
                                ============================================= -->
                        <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe">
                            <img src="/static/xsite_template/all_templates/xsite_template_six/images/sections/video.jpg"
                                 alt="Youtube Video" class="image_fade"
                                 style="box-shadow: 0px 0px 25px 0px rgba(0,0,0,0.15); border-radius: 6px;">
                            <i class="fa fa-play"
                               style="position: absolute; top: 50%; left: 50%; font-size: 60px; color: #FFF; margin-top: -45px; margin-left: -23px"></i>
                        </a>
                    </div>
                    <!-- Video Texts
                            ============================================= -->
                    <div class="col-lg-6" style="padding-left: 22px;">
                        <div class="heading-block topmargin-sm bottommargin-sm noborder">
                            <h3 class="nott"
                                style="font-size: 46px; font-weight: 700; letter-spacing: -2px; line-height: 58px"
                                id="video_title">
                                Video </h3>
                        </div>
                        <p class="t400" id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                            accusantium
                            doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et
                            quasi
                            architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                            aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                            voluptatem
                            sequi nesciunt?

                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Parallax Area
            ============================================= -->
    <section id="terminals_form">
        <div id="Testimonials" class="section parallax topmargin-lg nobottommargin notopborder clearfix"
             style="padding-bottom: 65px;padding-top: 65px; background-color: #18181A; margin-top: 0px !important;">
            <div class="container clearfix">

                <div class="row cleafix mt-10">
                    <div class="col-lg-4">

                        <div class="card shadow-sm">
                            <div class="card-body">
                                <div class="card shadow-sm">
                                    <div class="card-body">
                                        <h4 class="mb-3">Get Deals First hand!! Submit your information!</h4>
                                        <form id="buyer_form" class="nobottommargin "
                                              name="template-contactform"
                                              method="post">
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-name-buyer">Name:<small>*</small></label>
                                                <input type="text"
                                                       name="fullname"
                                                       id="template-contactform-name-buyer"
                                                       class="form-control input-sm required">
                                            </div>

                                            <div class="col_full mb-3">
                                                <label for="template-contactform-email-buyer">Email
                                                    Address:<small>*</small></label>
                                                <input type="email"
                                                       name="email"
                                                       class="form-control input-sm required"
                                                       id="template-contactform-email-buyer">
                                            </div>
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-phone-buyer">Phone:<small>*</small></label>
                                                <input type="text" id="template-contactform-phone-buyer"
                                                       name="phone"
                                                       class="form-control input-sm required">

                                            </div>

                                            <div class="col_full mb-3">
                                                <label for="template-contactform-service-buyer">What are you
                                                    looking
                                                    for?</label>
                                                <select id="template-contactform-service-buyer"
                                                        name="what_are_you_looking_for"
                                                        class="form-control input-sm required">
                                                    <option value="">What are you looking for?</option>
                                                </select>

                                            </div>
                                            <input type="hidden" name="audience" value="Buyer">
                                            <div class="col_full nobottommargin">
                                                <button class="button button-rounded btn-block nott ls0 m-0"
                                                        type="submit"
                                                        name="template-contactform-submit"
                                                        id="template-contactform-submit-buyer"
                                                        value="submit"> Get Your Ebook
                                                </button>
                                            </div>

                                        </form>
                                        <form id="seller_form" class="nobottommargin "
                                              name="template-contactform"
                                              method="post">
                                            <input type="hidden" name="audience" value="Seller">
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-name-seller">Name:<small>*</small></label>
                                                <input type="text" id="template-contactform-name-seller"
                                                       name="fullname"
                                                       class="form-control input-sm required"/>
                                            </div>
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-phone-seller">Phone:<small>*</small></label>
                                                <input type="text" id="template-contactform-phone-seller"
                                                       name="phone"
                                                       class="form-control input-sm required"/>
                                            </div>
                                            <div class="col_full mb-3">
                                                <label for="template-contactform-email-seller">Email
                                                    Address:<small>*</small></label>
                                                <input type="email" id="template-contactform-email-seller"
                                                       name="email"
                                                       class="form-control input-sm required"/>
                                            </div>

                                            <div class="col_full mb-3">

                                                <div class="form-check">
                                                    <label class="form-check-label">

                                                        <input name="immediate_assistance"
                                                               id="immediate_assistance"
                                                               type="checkbox"
                                                               class="form-check-input"
                                                               onclick="javascript:ShowFields()">

                                                        I
                                                        would like
                                                        immediate assistance
                                                    </label>
                                                </div>
                                            </div>

                                            <div id="immediate_assistance_fields" style="display: none">
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-address-seller">Street
                                                        Address:</label>
                                                    <input type="text"
                                                           id="template-contactform-address-seller"
                                                           name="street_address"
                                                           class="form-control input-sm required"/>
                                                </div>

                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-city-seller">City:</label>
                                                    <input type="text" id="template-contactform-city-seller"
                                                           name="city"
                                                           class="form-control input-sm required"/>
                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-state-seller">State:</label>
                                                    <select id="template-contactform-state-seller"
                                                            name="state"
                                                            class="form-control input-sm required">
                                                        <option value="">State</option>
                                                        <option value="AL">
                                                            Alabama
                                                        </option>
                                                        <option value="AK">
                                                            Alaska
                                                        </option>
                                                        <option value="AB">
                                                            Alberta
                                                        </option>
                                                        <option value="AS">
                                                            American Samoa
                                                        </option>
                                                        <option value="AZ">
                                                            Arizona
                                                        </option>
                                                        <option value="AR">
                                                            Arkansas
                                                        </option>
                                                        <option value="BC">
                                                            British Columbia
                                                        </option>
                                                        <option value="CA">
                                                            California
                                                        </option>
                                                        <option value="CO">
                                                            Colorado
                                                        </option>
                                                        <option value="CT">
                                                            Connecticut
                                                        </option>
                                                        <option value="DE">
                                                            Delaware
                                                        </option>
                                                        <option value="FM">
                                                            Fed. St. of Micronesia
                                                        </option>
                                                        <option value="FL">
                                                            Florida
                                                        </option>
                                                        <option value="GA">
                                                            Georgia
                                                        </option>
                                                        <option value="GU">
                                                            Guam
                                                        </option>
                                                        <option value="HI">
                                                            Hawaii
                                                        </option>
                                                        <option value="ID">
                                                            Idaho
                                                        </option>
                                                        <option value="IL">
                                                            Illinois
                                                        </option>
                                                        <option value="IN">
                                                            Indiana
                                                        </option>
                                                        <option value="IA">
                                                            Iowa
                                                        </option>
                                                        <option value="KS">
                                                            Kansas
                                                        </option>
                                                        <option value="KY">
                                                            Kentucky
                                                        </option>
                                                        <option value="LA">
                                                            Louisiana
                                                        </option>
                                                        <option value="ME">
                                                            Maine
                                                        </option>
                                                        <option value="MB">
                                                            Manitoba
                                                        </option>
                                                        <option value="MH">
                                                            Marshall Islands
                                                        </option>
                                                        <option value="MD">
                                                            Maryland
                                                        </option>
                                                        <option value="MA">
                                                            Massachusetts
                                                        </option>
                                                        <option value="MI">
                                                            Michigan
                                                        </option>
                                                        <option value="MN">
                                                            Minnesota
                                                        </option>
                                                        <option value="MS">
                                                            Mississippi
                                                        </option>
                                                        <option value="MO">
                                                            Missouri
                                                        </option>
                                                        <option value="MT">
                                                            Montana
                                                        </option>
                                                        <option value="NE">
                                                            Nebraska
                                                        </option>
                                                        <option value="NV">
                                                            Nevada
                                                        </option>
                                                        <option value="NB">
                                                            New Brunswick
                                                        </option>
                                                        <option value="NH">
                                                            New Hampshire
                                                        </option>
                                                        <option value="NJ">
                                                            New Jersey
                                                        </option>
                                                        <option value="NM">
                                                            New Mexico
                                                        </option>
                                                        <option value="NY">
                                                            New York
                                                        </option>
                                                        <option value="NL">
                                                            Newfoundland
                                                        </option>
                                                        <option value="NC">
                                                            North Carolina
                                                        </option>
                                                        <option value="ND">
                                                            North Dakota
                                                        </option>
                                                        <option value="MP">
                                                            Northern Mariana Islands
                                                        </option>
                                                        <option value="NT">
                                                            Northwest Territory
                                                        </option>
                                                        <option value="NS">
                                                            Nova Scotia
                                                        </option>
                                                        <option value="NU">
                                                            Nunavut
                                                        </option>
                                                        <option value="OH">
                                                            Ohio
                                                        </option>
                                                        <option value="OK">
                                                            Oklahoma
                                                        </option>
                                                        <option value="ON">
                                                            Ontario
                                                        </option>
                                                        <option value="OR">
                                                            Oregon
                                                        </option>
                                                        <option value="PA">
                                                            Pennsylvania
                                                        </option>
                                                        <option value="PE">
                                                            Prince Edward Island
                                                        </option>
                                                        <option value="PR">
                                                            Puerto Rico
                                                        </option>
                                                        <option value="QC">
                                                            Quebec
                                                        </option>
                                                        <option value="RI">
                                                            Rhode Island
                                                        </option>
                                                        <option value="SK">
                                                            Saskatchewan
                                                        </option>
                                                        <option value="SC">
                                                            South Carolina
                                                        </option>
                                                        <option value="SD">
                                                            South Dakota
                                                        </option>
                                                        <option value="TN">
                                                            Tennessee
                                                        </option>
                                                        <option value="TX">
                                                            Texas
                                                        </option>
                                                        <option value="UT">
                                                            Utah
                                                        </option>
                                                        <option value="VT">
                                                            Vermont
                                                        </option>
                                                        <option value="VI">
                                                            Virgin Islands
                                                        </option>
                                                        <option value="VA">
                                                            Virginia
                                                        </option>
                                                        <option value="WA">
                                                            Washington
                                                        </option>
                                                        <option value="DC">
                                                            Washington DC
                                                        </option>
                                                        <option value="WV">
                                                            West Virginia
                                                        </option>
                                                        <option value="WI">
                                                            Wisconsin
                                                        </option>
                                                        <option value="WY">
                                                            Wyoming
                                                        </option>
                                                        <option value="YT">
                                                            Yukon Territory
                                                        </option>
                                                    </select>
                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-zip-seller">Zip/Postal
                                                        Code:</label>
                                                    <input type="text" id="template-contactform-zip-seller"
                                                           name="zip"
                                                           class="form-control input-sm required"/>

                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-is_home_listed-seller">
                                                        Is
                                                        home
                                                        listed?</label>
                                                    <select id="template-contactform-is_home_listed-seller"
                                                            name="is_home_listed"
                                                            class="form-control input-sm required">
                                                        <option value="">Is home listed?</option>
                                                    </select>
                                                </div>
                                                <div class="col_full mb-3">
                                                    <label for="template-contactform-asking_price-seller">Asking
                                                        Price:</label>
                                                    <input type="number"
                                                           id="template-contactform-asking_price-seller"
                                                           name="asking_price"
                                                           class="form-control input-sm required" min="0"/>
                                                </div>
                                            </div>
                                            <div class="col_full nobottommargin">
                                                <button class="button button-rounded btn-block nott ls0 m-0"
                                                        type="submit"
                                                        name="template-contactform-submit"
                                                        id="template-contactform-seller"
                                                        value="submit"> GET your book
                                                </button>
                                            </div>

                                        </form>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>

                    <div class="topmargin d-block d-lg-none d-xl-block"></div>


                    <div class="col-lg-7 offset-lg-1 col-md-12 mt-4">
                        <h4 class="dark ">Testimonials</h4>
                        <div class="fslider testimonial" data-animation="slide" data-arrows="false">
                            <div id="testimonial_class" class="testimonial_class flexslider">
                                <div class="slider-wrap">
                                    <div class="slide">
                                        <div class="testimonial noborder noshadow">
                                            <div class="testi-content">
                                                <p class="bottommargin-sm font-primary" id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                <div class="testi-meta">
                                                    <span id="testi_1_person_name">Person 1</span>
                                                    <span  id="testi_1_company_name">Argon Tech 1</span>
                                                    <div class="testimonials-rating">
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                        <i class="fa fa-star"></i>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                        <div class="slide">
                                            <div class="testimonial noborder noshadow">
                                                <div class="testi-content">
                                                    <p class="bottommargin-sm font-primary" id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                    <div class="testi-meta">
                                                         <span id="testi_2_person_name">Person 1</span>
                                                         <span  id="testi_2_company_name">Argon Tech 1</span>
                                                        <div class="testimonials-rating">
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="slide">
                                            <div class="testimonial noborder noshadow">
                                                <div class="testi-content">
                                                    <p class="bottommargin-sm font-primary" id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                    inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                                    ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                                    <div class="testi-meta">
                                                        <span id="testi_3_person_name">Person 1</span>
                                                        <span  id="testi_3_company_name">Argon Tech 1</span>
                                                        <div class="testimonials-rating">
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                            <i class="fa fa-star"></i>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- Team Work
            ============================================= -->
    <div class="section nobg nobottompadding nobottommargin clearfix " id="Details"
         style="margin: 0; padding-top: 65px;">
        <div class="container clearfix">
            <div class="row clearfix">

                <div class="col-lg-6 order-lg-12">
                    <div class="device-xl device-md topmargin-lg"></div>
                    <h3 class="nobottommargin" style="font-size: 40px;" id="other_details_title">More To Know Us</h3>
                    <h3 class=" ls4 lowercase" style="font-size: 15px; color: #999;"></h3>
                    <p style="font-size: 20px;color: #888888; font-weight: 4;" id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
                    </p>
                </div>

                <div class="col-lg-6 order-lg-1">
                    <div style="position: relative; margin-bottom: 0;" class="ohidden" data-height-xl="520"
                         data-height-lg="520" data-height-md="520" data-height-sm="500" data-height-xs="300">
                        <img class="man ml-2"
                             src="/static/xsite_template/all_templates/xsite_template_six/images/sections/student_PNG62555.png"
                             style="position: absolute; top: 0; left: auto;" alt="Chrome">
                    </div>
                </div>

            </div>
        </div>
    </div>


</div>

</section>
<!-- #content end -->

<!-- Footer
    ============================================= -->
<footer id="#" class="noborder" style="padding: 30px 0; background-color: #000">

    <div class="container clearfix">
        <div class="col_two_third clearfix" style="margin: 0px;">
            <small class="t300" style="color: #fff">&copy; 2020 <strong><a class="text-dark"
                                                                           style="color: #fff !important"
                                                                           href="https://prospectx.com/"
                                                                           target="_blank">Prospectx</a></strong>
                All Rights Reserved.</small>
        </div>


    </div>

</footer>


</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script>
    // Owl Carousel Scripts
    $('#oc-features').owlCarousel({
        items: 1,
        margin: 60,
        nav: true,
        navText: ['<i class="fa fa-arrow-left"></i>', '<i class="fa fa-arrow-right"></i>'],
        dots: false,
        stagePadding: 30,
        responsive: {
            768: {items: 2},
            1200: {stagePadding: 200}
        },
    });
</script>
<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>
</body>"""

    Educational_head = """<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta name="author" content="SemiColonWeb"/>
    <title>Xsite</title>

    <!-- Stylesheets
    ============================================= -->
    <link href="http://fonts.googleapis.com/css?family=Istok+Web:400,700" rel="stylesheet" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>

    <link rel="stylesheet" href="/static/xsite_template/css/colors.php?color=0474c4" type="text/css"/>

    <!-- Hosting Demo Specific Stylesheet -->
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_seven/css/fonts.css"
          type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_seven/course.css"
          type="text/css"/>
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">
    <!-- / -->

</head>"""
    Educational_body = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <!-- Top Bar
   ============================================= -->
    <div id="top-bar" class="  dark">

        <div class="container clearfix">

            <div class="row justify-content-between">
                <div class="col-md-2">
                    <div class="top-links">
                        <ul class="sf-js-enabled clearfix" style="touch-action: pan-y;">
                            <li class=""><a href="#Form_page"
                                            class="sf-with-ul text-Carrot banner_button_text">Get your ebook</a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="col-md-10 d-flex justify-content-center justify-content-md-end">


                    <div id="top-social">
                        <ul>
                            <li><a href="#" class="si-facebook"><span class="ts-icon"><i
                                    class="fab fa-facebook-f"></i></span><span
                                    class="ts-text">Facebook</span></a></li>
                            <li><a href="#" class="si-twitter"><span class="ts-icon"><i
                                    class="fab fa-twitter"></i></span><span class="ts-text">Twitter</span></a>
                            </li>
                            <li><a href="#" class="si-instagram"><span class="ts-icon"><i
                                    class="fab fa-instagram"></i></span><span
                                    class="ts-text">Instagram</span></a></li>
                            <li><a href="tel:+91.11.85412542" class="si-call"><span class="ts-icon"><i
                                    class="fa fa-phone fa-flip-horizontal"></i></span><span
                                    class="ts-text" id="phone">03334455667</span></a></li>
                            <li><a href="mailto:info@xsite.com" class="si-email3"><span class="ts-icon"><i
                                    class="fa fa-envelope"></i></span><span
                                    class="ts-text" id="email">support@gmail.com</span></a></li>
                        </ul>
                    </div>

                </div>
            </div>

        </div>

    </div>

    <!-- Header
    ============================================= -->
    <header class="sticky-style-2 bg-light" id="home">

        <div class="container  clearfix">

            <nav class="navbar navbar-expand-lg p-0 m-0">
                <div id="logo">
                    <a href="#" class="standard-logo"><img class="logo_img"
                                                           src="/media/xsite_images/website_logos/prospectx-logo.png"
                                                           alt="Canvas Logo"></a>
                    <a href="#" class="retina-logo">
                        <img class="logo_img" src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Logo">
                    </a>
                </div>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="fa fa-bars"></span>
                </button>
                <div class="collapse navbar-collapse align-items-end template_seven_custom_color" id="navbarNav">
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item active">
                            <a class="nav-link" href="#home">Home</a>
                        </li>
                        <li class="nav-item">
                            <a href="#about" class="nav-link">About</a>
                        </li>
                        <li class="nav-item">
                            <a href="#Testimonials" class="nav-link">Testimonials</a>
                        </li>
                        <li class="nav-item">
                            <a href="#details" class="nav-link">Details</a>
                        </li>
                    </ul>
                </div>
            </nav>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element slider-parallax clearfix" style="height: 700px;">

        <!-- HTML5 Video Wrap
        ============================================= -->
        <div class="video-wrap">
            <video id="slide-video"
                   poster="/static/xsite_template/all_templates/xsite_template_seven/images/video/banner.jpg"
                   preload="auto" loop autoplay muted>
                <source src='#' type='video/mp4'/>
            </video>
            <div class="video-overlay" style="background: rgba(0,0,0,0.5); z-index: 1"></div>
        </div>

        <div class="vertical-middle center">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-10">
                        <div class="slider-title mb-2 dark clearfix">
                            <h2 class="text-white text-rotater mb-2 text-capitalize" data-separator=","
                                data-rotate="fadeIn" data-speed="3500" id="banner_title">Find Your Dream Home Here!
                                Beautiful Homes At Ugly Home Prices.</h2>
                        </div>
                        <div class="clear"></div>
                        <div class=" mt-1 text-center">
                            <a href="#Form_page"
                               class="button button-rounded button-xlarge bg-Carrot ls0 ls0 nott t400 nomargin banner_button_text">Get
                                your ebook</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </section>

    <!-- Content
    ============================================= -->
    <section id="content" style="overflow: visible;">

        <div class="content-wrap">

            <!-- About section
            ============================================= -->
            <div class="wave-bottom"
                 style="position: absolute; top: -12px; left: 0; width: 100%; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/wave-3.svg'); height: 12px; z-index: 2; background-repeat: repeat-x; transform: rotate(180deg);">
            </div>

            <div class="container" id="about">

                <div class="heading-block nobottomborder my-4 center">
                    <h3 id="about_us_title">Little More Detail About Us</h3>
                    <span id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</span>
                </div>
                <div class="clear"></div>

            </div>

            <!-- Form sections
            ============================================= -->
            <div id="Form_page" class="section mt-5 mb-0"
                 style="padding: 120px 0; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/icon-pattern-bg.jpg'); background-size: auto; background-repeat: repeat"
            >

                <!-- Wave Shape
                ============================================= -->
                <div class="wave-top"
                     style="position: absolute; top: 0; left: 0; width: 100%; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/wave-3.svg'); height: 12px; z-index: 2; background-repeat: repeat-x;">
                </div>

                <div class="container">
                    <div class="row">

                        <div class="col-lg-8">
                            <div class="row dark clearfix">

                                <!-- Feature - 1
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fa fa-university noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">BANKRUPTCY</h3>
                                            <p class="text-white">Houses where the owner is bankrupt and the house need to be sold immediately.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Feature - 2
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fas fa-balance-scale-right noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">DIVORCE</h3>
                                            <p class="text-white">Houses that need to be sold because of a recent divorce and the house is unwanted.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Feature - 3
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fa fa-sticky-note noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">TITLE ISSUES</h3>
                                            <p class="text-white">Houses where the owner has signed a bad title and the owner can’t afford payments.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Feature - 4
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fab fa-black-tie noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">RETIREMENT</h3>
                                            <p class="text-white">Houses where the owner(s) are in the process of downsizing due to retirement.</p>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>

                        <!-- Registration Form
                        ============================================= -->
                        <div class="col-lg-4">

                            <div class="card shadow" data-animate="shake" style="opacity: 1 !important">
                                <div class="card-body">

                                    <div class="badge registration-badge shadow-sm alert-primary"
                                         style="background-color: #FC9928;">FREE
                                    </div>
                                    <h4 class="card-title ls-1 mt-4 t700 h5" id="banner_title1">Find Your Dream Home
                                        Here! Beautiful Homes At Ugly Home Prices.</h4>
                                    <h6 class="card-subtitle mb-4 t400 uppercase ls2 text-black-50">Free
                                        Registration here.</h6>

                                    <div class="form-widget">
                                        <div class="form-result"></div>
                                        <form id="buyer_form" class="nobottommargin"
                                              name="template-contactform"
                                              method="post">

                                            <div class="form-process"></div>
                                            <div class="col_full">
                                                <input type="text"
                                                       id="template-contactform-name"
                                                       name="fullname"
                                                       class="sm-form-control border-form-control required"
                                                       placeholder="Your Full Name:"/>
                                            </div>

                                            <div class="col_full">
                                                <input type="email"
                                                       name="email"
                                                       class="required email sm-form-control border-form-control"
                                                       placeholder="Your Email Address:"
                                                       id="template-contactform-email-buyer">
                                            </div>
                                            <div class="col_full">
                                                <input type="text" id="template-contactform-phone-buyer"
                                                       name="phone"
                                                       class="sm-form-control border-form-control required"
                                                       placeholder="Your Phone Number:">

                                            </div>

                                            <div class="col_full">
                                                <select id="template-contactform-service-buyer"
                                                        name="what_are_you_looking_for"
                                                        class="sm-form-control border-form-control required">
                                                    <option value="">What are you looking for?</option>
                                                </select>

                                            </div>
                                            <input type="hidden" name="audience" value="Buyer">

                                            <div class="col_full">
                                                <button
                                                        class="button button-rounded btn-block button-large bgcolor text-white nott ls0 bg-Carrot"
                                                        style="margin-left: 0px;" type="submit"
                                                        id="template-contactform-submit-buyer"
                                                        name="template-contactform-submit"
                                                        value="submit">Get your ebook
                                                </button>
                                                <br>
                                                <small
                                                        style="display: block; font-size: 12px; margin-top: 15px; color: #AAA;"><em>We'll
                                                    do our best to get back to you within 6-8 working
                                                    hours.</em></small>
                                            </div>

                                            <div class="clear"></div>

                                        </form>
                                        <form id="seller_form" class="nobottommargin "
                                              name="template-contactform"
                                              method="post">

                                            <div class="form-process"></div>
                                            <input type="hidden" name="audience" value="Seller">
                                            <div class="col_full">
                                                <input type="text" id="template-contactform-name-seller"
                                                       name="fullname"
                                                       placeholder="Your Full Name:"
                                                       class="sm-form-control border-form-control required"/>
                                            </div>
                                            <div class="col_full">
                                                <input type="text" id="template-contactform-phone-seller"
                                                       name="phone"
                                                       placeholder="Your Phone Number:"
                                                       class="sm-form-control border-form-control required"/>
                                            </div>
                                            <div class="col_full">
                                                <input type="email" id="template-contactform-email-seller"
                                                       name="email"
                                                       placeholder="Your Email Address:"
                                                       class="sm-form-control border-form-control required"/>
                                            </div>

                                            <div class="col_full">

                                                <div class="form-check">
                                                    <label class="form-check-label">

                                                        <input name="immediate_assistance"
                                                               id="immediate_assistance"
                                                               type="checkbox"
                                                               class="form-check-input"
                                                               onclick="javascript:ShowFields()">

                                                        I
                                                        would like
                                                        immediate assistance
                                                    </label>
                                                </div>
                                            </div>

                                            <div id="immediate_assistance_fields" style="display: none">
                                                <div class="col_full">
                                                    <input type="text"
                                                           id="template-contactform-address-seller"
                                                           name="street_address"
                                                           placeholder="Your Street Address:"
                                                           class="sm-form-control border-form-control required"/>
                                                </div>

                                                <div class="col_full">
                                                    <input type="text" id="template-contactform-city-seller"
                                                           name="city"
                                                           placeholder="Your City:"
                                                           class="sm-form-control border-form-control required"/>
                                                </div>
                                                <div class="col_full">
                                                    <select id="template-contactform-state-seller"
                                                            name="state"
                                                            class="sm-form-control border-form-control required">
                                                        <option value="">State</option>
                                                        <option value="AL">
                                                            Alabama
                                                        </option>
                                                        <option value="AK">
                                                            Alaska
                                                        </option>
                                                        <option value="AB">
                                                            Alberta
                                                        </option>
                                                        <option value="AS">
                                                            American Samoa
                                                        </option>
                                                        <option value="AZ">
                                                            Arizona
                                                        </option>
                                                        <option value="AR">
                                                            Arkansas
                                                        </option>
                                                        <option value="BC">
                                                            British Columbia
                                                        </option>
                                                        <option value="CA">
                                                            California
                                                        </option>
                                                        <option value="CO">
                                                            Colorado
                                                        </option>
                                                        <option value="CT">
                                                            Connecticut
                                                        </option>
                                                        <option value="DE">
                                                            Delaware
                                                        </option>
                                                        <option value="FM">
                                                            Fed. St. of Micronesia
                                                        </option>
                                                        <option value="FL">
                                                            Florida
                                                        </option>
                                                        <option value="GA">
                                                            Georgia
                                                        </option>
                                                        <option value="GU">
                                                            Guam
                                                        </option>
                                                        <option value="HI">
                                                            Hawaii
                                                        </option>
                                                        <option value="ID">
                                                            Idaho
                                                        </option>
                                                        <option value="IL">
                                                            Illinois
                                                        </option>
                                                        <option value="IN">
                                                            Indiana
                                                        </option>
                                                        <option value="IA">
                                                            Iowa
                                                        </option>
                                                        <option value="KS">
                                                            Kansas
                                                        </option>
                                                        <option value="KY">
                                                            Kentucky
                                                        </option>
                                                        <option value="LA">
                                                            Louisiana
                                                        </option>
                                                        <option value="ME">
                                                            Maine
                                                        </option>
                                                        <option value="MB">
                                                            Manitoba
                                                        </option>
                                                        <option value="MH">
                                                            Marshall Islands
                                                        </option>
                                                        <option value="MD">
                                                            Maryland
                                                        </option>
                                                        <option value="MA">
                                                            Massachusetts
                                                        </option>
                                                        <option value="MI">
                                                            Michigan
                                                        </option>
                                                        <option value="MN">
                                                            Minnesota
                                                        </option>
                                                        <option value="MS">
                                                            Mississippi
                                                        </option>
                                                        <option value="MO">
                                                            Missouri
                                                        </option>
                                                        <option value="MT">
                                                            Montana
                                                        </option>
                                                        <option value="NE">
                                                            Nebraska
                                                        </option>
                                                        <option value="NV">
                                                            Nevada
                                                        </option>
                                                        <option value="NB">
                                                            New Brunswick
                                                        </option>
                                                        <option value="NH">
                                                            New Hampshire
                                                        </option>
                                                        <option value="NJ">
                                                            New Jersey
                                                        </option>
                                                        <option value="NM">
                                                            New Mexico
                                                        </option>
                                                        <option value="NY">
                                                            New York
                                                        </option>
                                                        <option value="NL">
                                                            Newfoundland
                                                        </option>
                                                        <option value="NC">
                                                            North Carolina
                                                        </option>
                                                        <option value="ND">
                                                            North Dakota
                                                        </option>
                                                        <option value="MP">
                                                            Northern Mariana Islands
                                                        </option>
                                                        <option value="NT">
                                                            Northwest Territory
                                                        </option>
                                                        <option value="NS">
                                                            Nova Scotia
                                                        </option>
                                                        <option value="NU">
                                                            Nunavut
                                                        </option>
                                                        <option value="OH">
                                                            Ohio
                                                        </option>
                                                        <option value="OK">
                                                            Oklahoma
                                                        </option>
                                                        <option value="ON">
                                                            Ontario
                                                        </option>
                                                        <option value="OR">
                                                            Oregon
                                                        </option>
                                                        <option value="PA">
                                                            Pennsylvania
                                                        </option>
                                                        <option value="PE">
                                                            Prince Edward Island
                                                        </option>
                                                        <option value="PR">
                                                            Puerto Rico
                                                        </option>
                                                        <option value="QC">
                                                            Quebec
                                                        </option>
                                                        <option value="RI">
                                                            Rhode Island
                                                        </option>
                                                        <option value="SK">
                                                            Saskatchewan
                                                        </option>
                                                        <option value="SC">
                                                            South Carolina
                                                        </option>
                                                        <option value="SD">
                                                            South Dakota
                                                        </option>
                                                        <option value="TN">
                                                            Tennessee
                                                        </option>
                                                        <option value="TX">
                                                            Texas
                                                        </option>
                                                        <option value="UT">
                                                            Utah
                                                        </option>
                                                        <option value="VT">
                                                            Vermont
                                                        </option>
                                                        <option value="VI">
                                                            Virgin Islands
                                                        </option>
                                                        <option value="VA">
                                                            Virginia
                                                        </option>
                                                        <option value="WA">
                                                            Washington
                                                        </option>
                                                        <option value="DC">
                                                            Washington DC
                                                        </option>
                                                        <option value="WV">
                                                            West Virginia
                                                        </option>
                                                        <option value="WI">
                                                            Wisconsin
                                                        </option>
                                                        <option value="WY">
                                                            Wyoming
                                                        </option>
                                                        <option value="YT">
                                                            Yukon Territory
                                                        </option>
                                                    </select>
                                                </div>
                                                <div class="col_full">
                                                    <input type="text" id="template-contactform-zip-seller"
                                                           name="zip"
                                                           placeholder="Your Zip Code:"
                                                           class="sm-form-control border-form-control required"/>

                                                </div>
                                                <div class="col_full mb-3">
                                                    <select id="template-contactform-is_home_listed-seller"
                                                            name="is_home_listed"
                                                            class="sm-form-control border-form-control required">
                                                        <option value="">Is home listed?</option>
                                                    </select>
                                                </div>
                                                <div class="col_full">
                                                    <input type="number"
                                                           id="template-contactform-asking_price-seller"
                                                           name="asking_price"
                                                           placeholder="Your Asking Price:"
                                                           class="sm-form-control border-form-control required"
                                                           min="0"/>
                                                </div>
                                            </div>
                                            <div class="col_full">
                                                <button
                                                        class="button button-rounded btn-block button-large bgcolor text-white nott ls0 bg-Carrot"
                                                        style="margin-left: 0px;" type="submit"
                                                        id="template-contactform-seller"
                                                        name="template-contactform-submit"
                                                        value="submit">Get your ebook
                                                </button>
                                                <br>
                                                <small
                                                        style="display: block; font-size: 12px; margin-top: 15px; color: #AAA;"><em>We'll
                                                    do our best to get back to you within 6-8 working
                                                    hours.</em></small>
                                            </div>

                                            <div class="clear"></div>

                                        </form>
                                    </div>

                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Wave Shape
                ============================================= -->
                <div class="wave-bottom"
                     style="position: absolute; top: auto; bottom: 0; left: 0; width: 100%; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/wave-3.svg'); height: 12px; z-index: 2; background-repeat: repeat-x; transform: rotate(180deg);">
                </div>

            </div>


            <!-- Vedio section
            ============================================= -->
            <div class="section m-0"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_seven/images/1.jpg') no-repeat center center; background-size: cover; padding: 100px 0;">
                <div class="container">
                    <div class="row justify-content-between align-items-center">

                        <div class="col-md-6">
                            <div class="heading-block nobottomborder bottommargin-sm">
                                <h3 class="nott vedio_section_heading" id="video_title">Video</h3>
                            </div>
                            <p id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                accusantium
                                doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et
                                quasi
                                architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas
                                sit
                                aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                                voluptatem
                                sequi nesciunt?</p>

                        </div>


                        <div class="col-md-4 mt-5 mt-md-0 center">
                            <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe"
                               class="play-icon shadow"><i class="fa fa-play"></i></a>
                        </div>

                    </div>

                </div>
            </div>

            <!-- testimonials Section
            ============================================= -->
            <div id="Testimonials" class="section mt-0"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_seven/images/icon-pattern.jpg') no-repeat top center; background-size: cover; padding: 80px 0 70px;">
                <div class="container">
                    <div class="heading-block nobottomborder center">
                        <h3 class="nott ls0">What Clients Says</h3>
                    </div>

                    <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget clearfix"
                         data-margin="0" data-pagi="true" data-loop="true" data-center="true" data-autoplay="5000"
                         data-items-sm="1" data-items-md="2" data-items-xl="3">

                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-content">
                                    <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                                        enim
                                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                        consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_1_person_name">Person 1</span>
                                        <span id="testi_1_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-content">
                                    <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                                        enim
                                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                        consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_2_person_name">Person 1</span>
                                        <span id="testi_2_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-content">
                                    <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                                        enim
                                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                        consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_3_person_name">Person 1</span>
                                        <span id="testi_3_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- More detrails Section
            ============================================= -->
            <div id="details" class="section m-0"
                 style="padding: 120px 0; background: #FFF url('/static/xsite_template/all_templates/xsite_template_seven/images/instructor.jpg') no-repeat left top / cover">
                <div class="container">
                    <div class="row">

                        <div class="col-md-7"></div>

                        <div class="col-md-5">
                            <div class="heading-block nobottomborder mb-4 mt-5">
                                <h3 id="other_details_title">More To Know Us</h3>
                            </div>
                            <p class="mb-2" id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit
                                voluptatem
                                accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                                veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam
                                voluptatem quia
                                voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui
                                ratione
                                voluptatem sequi nesciunt?</p>
                        </div>

                    </div>
                </div>
            </div>

            <div class="promo promo-light promo-full footer-stick" style="padding: 30px 0 !important;">
                <div class="container clearfix">
                    <h3 class="ls-1 ">Call us today at <span style="color: orange;" class="phone">03334455667</span> or
                        Email us
                        at
                        <span style="color: orange;" class="email">support@gmail.com</span></h3>
                    <!-- <span class="text-black-50">We strive to provide Our Customers with Top Notch Support to make their Theme Experience Wonderful.</span> -->
                    <a href="#Form_page"
                       class="button button-xlarge button-rounded nott ls0 t400  bg-Carrot banner_button_text">Get your
                        ebook</a>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="dark">
        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="pt-2 pb-2">

            <div class="container clearfix">

                <div class="row align-items-center justify-content-between">
                    <div class="col-md-6">
                        &copy; 2020 <strong><a href="https://prospectx.com/"
                                               target="_blank" style="color: orange;">Prospectx</a></strong> All Rights
                        Reserved.<br>
                    </div>
                </div>

            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->
</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="icon-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>
</body>"""

    Educational_body_seller = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <!-- Top Bar
   ============================================= -->
    <div id="top-bar" class="  dark">

        <div class="container clearfix">

            <div class="row justify-content-between">
                <div class="col-md-2">
                    <div class="top-links">
                        <ul class="sf-js-enabled clearfix" style="touch-action: pan-y;">
                            <li class=""><a href="#Form_page"
                                            class="sf-with-ul text-Carrot banner_button_text">Get your ebook</a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="col-md-10 d-flex justify-content-center justify-content-md-end">


                    <div id="top-social">
                        <ul>
                            <li><a href="#" class="si-facebook"><span class="ts-icon"><i
                                    class="fab fa-facebook-f"></i></span><span
                                    class="ts-text">Facebook</span></a></li>
                            <li><a href="#" class="si-twitter"><span class="ts-icon"><i
                                    class="fab fa-twitter"></i></span><span class="ts-text">Twitter</span></a>
                            </li>
                            <li><a href="#" class="si-instagram"><span class="ts-icon"><i
                                    class="fab fa-instagram"></i></span><span
                                    class="ts-text">Instagram</span></a></li>
                            <li><a href="tel:+91.11.85412542" class="si-call"><span class="ts-icon"><i
                                    class="fa fa-phone fa-flip-horizontal"></i></span><span
                                    class="ts-text" id="phone">03334455667</span></a></li>
                            <li><a href="mailto:info@xsite.com" class="si-email3"><span class="ts-icon"><i
                                    class="fa fa-envelope"></i></span><span
                                    class="ts-text" id="email">support@gmail.com</span></a></li>
                        </ul>
                    </div>

                </div>
            </div>

        </div>

    </div>

    <!-- Header
    ============================================= -->
    <header class="sticky-style-2 bg-light" id="home">

        <div class="container  clearfix">

            <nav class="navbar navbar-expand-lg p-0 m-0">
                <div id="logo">
                    <a href="#" class="standard-logo"><img class="logo_img"
                                                           src="/media/xsite_images/website_logos/prospectx-logo.png"
                                                           alt="Canvas Logo"></a>
                    <a href="#" class="retina-logo">
                        <img class="logo_img" src="/media/xsite_images/website_logos/prospectx-logo.png" alt="Logo">
                    </a>
                </div>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="fa fa-bars"></span>
                </button>
                <div class="collapse navbar-collapse align-items-end template_seven_custom_color" id="navbarNav">
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item active">
                            <a class="nav-link" href="#home">Home</a>
                        </li>
                        <li class="nav-item">
                            <a href="#about" class="nav-link">About</a>
                        </li>
                        <li class="nav-item">
                            <a href="#Testimonials" class="nav-link">Testimonials</a>
                        </li>
                        <li class="nav-item">
                            <a href="#details" class="nav-link">Details</a>
                        </li>
                    </ul>
                </div>
            </nav>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="slider" class="slider-element slider-parallax clearfix" style="height: 700px;">

        <!-- HTML5 Video Wrap
        ============================================= -->
        <div class="video-wrap">
            <video id="slide-video"
                   poster="/static/xsite_template/all_templates/xsite_template_seven/images/video/banner.jpg"
                   preload="auto" loop autoplay muted>
                <source src='#' type='video/mp4'/>
            </video>
            <div class="video-overlay" style="background: rgba(0,0,0,0.5); z-index: 1"></div>
        </div>

        <div class="vertical-middle center">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-10">
                        <div class="slider-title mb-2 dark clearfix">
                            <h2 class="text-white text-rotater mb-2 text-capitalize" data-separator=","
                                data-rotate="fadeIn" data-speed="3500" id="banner_title">Find Your Dream Home Here!
                                Beautiful Homes At Ugly Home Prices.</h2>
                        </div>
                        <div class="clear"></div>
                        <div class=" mt-1 text-center">
                            <a href="#Form_page"
                               class="button button-rounded button-xlarge bg-Carrot ls0 ls0 nott t400 nomargin banner_button_text">Get
                                your ebook</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </section>

    <!-- Content
    ============================================= -->
    <section id="content" style="overflow: visible;">

        <div class="content-wrap">

            <!-- About section
            ============================================= -->
            <div class="wave-bottom"
                 style="position: absolute; top: -12px; left: 0; width: 100%; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/wave-3.svg'); height: 12px; z-index: 2; background-repeat: repeat-x; transform: rotate(180deg);">
            </div>

            <div class="container" id="about">

                <div class="heading-block nobottomborder my-4 center">
                    <h3 id="about_us_title">Little More Detail About Us</h3>
                    <span id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</span>
                </div>
                <div class="clear"></div>

            </div>

            <!-- Form sections
            ============================================= -->
            <div id="Form_page" class="section mt-5 mb-0"
                 style="padding: 120px 0; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/icon-pattern-bg.jpg'); background-size: auto; background-repeat: repeat"
            >

                <!-- Wave Shape
                ============================================= -->
                <div class="wave-top"
                     style="position: absolute; top: 0; left: 0; width: 100%; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/wave-3.svg'); height: 12px; z-index: 2; background-repeat: repeat-x;">
                </div>

                <div class="container">
                    <div class="row">

                        <div class="col-lg-8">
                            <div class="row dark clearfix">

                                <!-- Feature - 1
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fa fa-building noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">EXCLUSIVE DEALS</h3>
                                            <p class="text-white">As a real estate investment firm, we pride ourselves on exclusive property deals.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Feature - 2
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fa fa-phone-volume noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">COMPLETE CONTROL</h3>
                                            <p class="text-white">We allow buyers to buy directly from the source so that they have complete control over the process. No middleman here!</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Feature - 3
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fa fa-sticky-note noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">THOUSANDS OF DEALS AND COUNTING</h3>
                                            <p class="text-white">Big opportunity! Thanks to countless property deals made over the years, we’ve built long-lasting relationships that all allow us to purchase properties for less.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Feature - 4
                                ============================================= -->
                                <div class="col-md-6">
                                    <div class="feature-box media-box bottommargin">
                                        <div class="fbox-icon">
                                            <a href="#">
                                                <i class="fa fa-city noradius nobg tleft"></i>
                                            </a>
                                        </div>
                                        <div class="fbox-desc">
                                            <h3 class="text-white">OUR GUARANTEE, NO BIDDING WARS</h3>
                                            <p class="text-white">We boast a first-come, first-serve policy. The first real estate investor to sign a contract and offer a deposit is the one to secure the property. No bidding up prices here!</p>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>

                        <!-- Registration Form
                        ============================================= -->
                        <div class="col-lg-4">

                            <div class="card shadow" data-animate="shake" style="opacity: 1 !important">
                                <div class="card-body">

                                    <div class="badge registration-badge shadow-sm alert-primary"
                                         style="background-color: #FC9928;">FREE
                                    </div>
                                    <h4 class="card-title ls-1 mt-4 t700 h5" id="banner_title1">Find Your Dream Home
                                        Here! Beautiful Homes At Ugly Home Prices.</h4>
                                    <h6 class="card-subtitle mb-4 t400 uppercase ls2 text-black-50">Free
                                        Registration here.</h6>

                                    <div class="form-widget">
                                        <div class="form-result"></div>
                                        <form id="buyer_form" class="nobottommargin"
                                              name="template-contactform"
                                              method="post">

                                            <div class="form-process"></div>
                                            <div class="col_full">
                                                <input type="text"
                                                       id="template-contactform-name"
                                                       name="fullname"
                                                       class="sm-form-control border-form-control required"
                                                       placeholder="Your Full Name:"/>
                                            </div>

                                            <div class="col_full">
                                                <input type="email"
                                                       name="email"
                                                       class="required email sm-form-control border-form-control"
                                                       placeholder="Your Email Address:"
                                                       id="template-contactform-email-buyer">
                                            </div>
                                            <div class="col_full">
                                                <input type="text" id="template-contactform-phone-buyer"
                                                       name="phone"
                                                       class="sm-form-control border-form-control required"
                                                       placeholder="Your Phone Number:">

                                            </div>

                                            <div class="col_full">
                                                <select id="template-contactform-service-buyer"
                                                        name="what_are_you_looking_for"
                                                        class="sm-form-control border-form-control required">
                                                    <option value="">What are you looking for?</option>
                                                </select>

                                            </div>
                                            <input type="hidden" name="audience" value="Buyer">

                                            <div class="col_full">
                                                <button
                                                        class="button button-rounded btn-block button-large bgcolor text-white nott ls0 bg-Carrot"
                                                        style="margin-left: 0px;" type="submit"
                                                        id="template-contactform-submit-buyer"
                                                        name="template-contactform-submit"
                                                        value="submit">Get your ebook
                                                </button>
                                                <br>
                                                <small
                                                        style="display: block; font-size: 12px; margin-top: 15px; color: #AAA;"><em>We'll
                                                    do our best to get back to you within 6-8 working
                                                    hours.</em></small>
                                            </div>

                                            <div class="clear"></div>

                                        </form>
                                        <form id="seller_form" class="nobottommargin "
                                              name="template-contactform"
                                              method="post">

                                            <div class="form-process"></div>
                                            <input type="hidden" name="audience" value="Seller">
                                            <div class="col_full">
                                                <input type="text" id="template-contactform-name-seller"
                                                       name="fullname"
                                                       placeholder="Your Full Name:"
                                                       class="sm-form-control border-form-control required"/>
                                            </div>
                                            <div class="col_full">
                                                <input type="text" id="template-contactform-phone-seller"
                                                       name="phone"
                                                       placeholder="Your Phone Number:"
                                                       class="sm-form-control border-form-control required"/>
                                            </div>
                                            <div class="col_full">
                                                <input type="email" id="template-contactform-email-seller"
                                                       name="email"
                                                       placeholder="Your Email Address:"
                                                       class="sm-form-control border-form-control required"/>
                                            </div>

                                            <div class="col_full">

                                                <div class="form-check">
                                                    <label class="form-check-label">

                                                        <input name="immediate_assistance"
                                                               id="immediate_assistance"
                                                               type="checkbox"
                                                               class="form-check-input"
                                                               onclick="javascript:ShowFields()">

                                                        I
                                                        would like
                                                        immediate assistance
                                                    </label>
                                                </div>
                                            </div>

                                            <div id="immediate_assistance_fields" style="display: none">
                                                <div class="col_full">
                                                    <input type="text"
                                                           id="template-contactform-address-seller"
                                                           name="street_address"
                                                           placeholder="Your Street Address:"
                                                           class="sm-form-control border-form-control required"/>
                                                </div>

                                                <div class="col_full">
                                                    <input type="text" id="template-contactform-city-seller"
                                                           name="city"
                                                           placeholder="Your City:"
                                                           class="sm-form-control border-form-control required"/>
                                                </div>
                                                <div class="col_full">
                                                    <select id="template-contactform-state-seller"
                                                            name="state"
                                                            class="sm-form-control border-form-control required">
                                                        <option value="">State</option>
                                                        <option value="AL">
                                                            Alabama
                                                        </option>
                                                        <option value="AK">
                                                            Alaska
                                                        </option>
                                                        <option value="AB">
                                                            Alberta
                                                        </option>
                                                        <option value="AS">
                                                            American Samoa
                                                        </option>
                                                        <option value="AZ">
                                                            Arizona
                                                        </option>
                                                        <option value="AR">
                                                            Arkansas
                                                        </option>
                                                        <option value="BC">
                                                            British Columbia
                                                        </option>
                                                        <option value="CA">
                                                            California
                                                        </option>
                                                        <option value="CO">
                                                            Colorado
                                                        </option>
                                                        <option value="CT">
                                                            Connecticut
                                                        </option>
                                                        <option value="DE">
                                                            Delaware
                                                        </option>
                                                        <option value="FM">
                                                            Fed. St. of Micronesia
                                                        </option>
                                                        <option value="FL">
                                                            Florida
                                                        </option>
                                                        <option value="GA">
                                                            Georgia
                                                        </option>
                                                        <option value="GU">
                                                            Guam
                                                        </option>
                                                        <option value="HI">
                                                            Hawaii
                                                        </option>
                                                        <option value="ID">
                                                            Idaho
                                                        </option>
                                                        <option value="IL">
                                                            Illinois
                                                        </option>
                                                        <option value="IN">
                                                            Indiana
                                                        </option>
                                                        <option value="IA">
                                                            Iowa
                                                        </option>
                                                        <option value="KS">
                                                            Kansas
                                                        </option>
                                                        <option value="KY">
                                                            Kentucky
                                                        </option>
                                                        <option value="LA">
                                                            Louisiana
                                                        </option>
                                                        <option value="ME">
                                                            Maine
                                                        </option>
                                                        <option value="MB">
                                                            Manitoba
                                                        </option>
                                                        <option value="MH">
                                                            Marshall Islands
                                                        </option>
                                                        <option value="MD">
                                                            Maryland
                                                        </option>
                                                        <option value="MA">
                                                            Massachusetts
                                                        </option>
                                                        <option value="MI">
                                                            Michigan
                                                        </option>
                                                        <option value="MN">
                                                            Minnesota
                                                        </option>
                                                        <option value="MS">
                                                            Mississippi
                                                        </option>
                                                        <option value="MO">
                                                            Missouri
                                                        </option>
                                                        <option value="MT">
                                                            Montana
                                                        </option>
                                                        <option value="NE">
                                                            Nebraska
                                                        </option>
                                                        <option value="NV">
                                                            Nevada
                                                        </option>
                                                        <option value="NB">
                                                            New Brunswick
                                                        </option>
                                                        <option value="NH">
                                                            New Hampshire
                                                        </option>
                                                        <option value="NJ">
                                                            New Jersey
                                                        </option>
                                                        <option value="NM">
                                                            New Mexico
                                                        </option>
                                                        <option value="NY">
                                                            New York
                                                        </option>
                                                        <option value="NL">
                                                            Newfoundland
                                                        </option>
                                                        <option value="NC">
                                                            North Carolina
                                                        </option>
                                                        <option value="ND">
                                                            North Dakota
                                                        </option>
                                                        <option value="MP">
                                                            Northern Mariana Islands
                                                        </option>
                                                        <option value="NT">
                                                            Northwest Territory
                                                        </option>
                                                        <option value="NS">
                                                            Nova Scotia
                                                        </option>
                                                        <option value="NU">
                                                            Nunavut
                                                        </option>
                                                        <option value="OH">
                                                            Ohio
                                                        </option>
                                                        <option value="OK">
                                                            Oklahoma
                                                        </option>
                                                        <option value="ON">
                                                            Ontario
                                                        </option>
                                                        <option value="OR">
                                                            Oregon
                                                        </option>
                                                        <option value="PA">
                                                            Pennsylvania
                                                        </option>
                                                        <option value="PE">
                                                            Prince Edward Island
                                                        </option>
                                                        <option value="PR">
                                                            Puerto Rico
                                                        </option>
                                                        <option value="QC">
                                                            Quebec
                                                        </option>
                                                        <option value="RI">
                                                            Rhode Island
                                                        </option>
                                                        <option value="SK">
                                                            Saskatchewan
                                                        </option>
                                                        <option value="SC">
                                                            South Carolina
                                                        </option>
                                                        <option value="SD">
                                                            South Dakota
                                                        </option>
                                                        <option value="TN">
                                                            Tennessee
                                                        </option>
                                                        <option value="TX">
                                                            Texas
                                                        </option>
                                                        <option value="UT">
                                                            Utah
                                                        </option>
                                                        <option value="VT">
                                                            Vermont
                                                        </option>
                                                        <option value="VI">
                                                            Virgin Islands
                                                        </option>
                                                        <option value="VA">
                                                            Virginia
                                                        </option>
                                                        <option value="WA">
                                                            Washington
                                                        </option>
                                                        <option value="DC">
                                                            Washington DC
                                                        </option>
                                                        <option value="WV">
                                                            West Virginia
                                                        </option>
                                                        <option value="WI">
                                                            Wisconsin
                                                        </option>
                                                        <option value="WY">
                                                            Wyoming
                                                        </option>
                                                        <option value="YT">
                                                            Yukon Territory
                                                        </option>
                                                    </select>
                                                </div>
                                                <div class="col_full">
                                                    <input type="text" id="template-contactform-zip-seller"
                                                           name="zip"
                                                           placeholder="Your Zip Code:"
                                                           class="sm-form-control border-form-control required"/>

                                                </div>
                                                <div class="col_full mb-3">
                                                    <select id="template-contactform-is_home_listed-seller"
                                                            name="is_home_listed"
                                                            class="sm-form-control border-form-control required">
                                                        <option value="">Is home listed?</option>
                                                    </select>
                                                </div>
                                                <div class="col_full">
                                                    <input type="number"
                                                           id="template-contactform-asking_price-seller"
                                                           name="asking_price"
                                                           placeholder="Your Asking Price:"
                                                           class="sm-form-control border-form-control required"
                                                           min="0"/>
                                                </div>
                                            </div>
                                            <div class="col_full">
                                                <button
                                                        class="button button-rounded btn-block button-large bgcolor text-white nott ls0 bg-Carrot"
                                                        style="margin-left: 0px;" type="submit"
                                                        id="template-contactform-seller"
                                                        name="template-contactform-submit"
                                                        value="submit">Get your ebook
                                                </button>
                                                <br>
                                                <small
                                                        style="display: block; font-size: 12px; margin-top: 15px; color: #AAA;"><em>We'll
                                                    do our best to get back to you within 6-8 working
                                                    hours.</em></small>
                                            </div>

                                            <div class="clear"></div>

                                        </form>
                                    </div>

                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Wave Shape
                ============================================= -->
                <div class="wave-bottom"
                     style="position: absolute; top: auto; bottom: 0; left: 0; width: 100%; background-image: url('/static/xsite_template/all_templates/xsite_template_seven/images/wave-3.svg'); height: 12px; z-index: 2; background-repeat: repeat-x; transform: rotate(180deg);">
                </div>

            </div>


            <!-- Vedio section
            ============================================= -->
            <div class="section m-0"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_seven/images/1.jpg') no-repeat center center; background-size: cover; padding: 100px 0;">
                <div class="container">
                    <div class="row justify-content-between align-items-center">

                        <div class="col-md-6">
                            <div class="heading-block nobottomborder bottommargin-sm">
                                <h3 class="nott vedio_section_heading" id="video_title">Video</h3>
                            </div>
                            <p id="video_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                accusantium
                                doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et
                                quasi
                                architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas
                                sit
                                aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                                voluptatem
                                sequi nesciunt?</p>

                        </div>


                        <div class="col-md-4 mt-5 mt-md-0 center">
                            <a id="video_link" href="https://www.youtube.com/watch?v=NS0txu_Kzl8" data-lightbox="iframe"
                               class="play-icon shadow"><i class="fa fa-play"></i></a>
                        </div>

                    </div>

                </div>
            </div>

            <!-- testimonials Section
            ============================================= -->
            <div id="Testimonials" class="section mt-0"
                 style="background: url('/static/xsite_template/all_templates/xsite_template_seven/images/icon-pattern.jpg') no-repeat top center; background-size: cover; padding: 80px 0 70px;">
                <div class="container">
                    <div class="heading-block nobottomborder center">
                        <h3 class="nott ls0">What Clients Says</h3>
                    </div>

                    <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget clearfix"
                         data-margin="0" data-pagi="true" data-loop="true" data-center="true" data-autoplay="5000"
                         data-items-sm="1" data-items-md="2" data-items-xl="3">

                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-content">
                                    <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                                        enim
                                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                        consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_1_person_name">Person 1</span>
                                        <span id="testi_1_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-content">
                                    <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                                        enim
                                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                        consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_2_person_name">Person 1</span>
                                        <span id="testi_2_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="oc-item">
                            <div class="testimonial">
                                <div class="testi-content">
                                    <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                                        enim
                                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                        consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                    <div class="testi-meta">
                                        <span id="testi_3_person_name">Person 1</span>
                                        <span id="testi_3_company_name">Argon Tech</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- More detrails Section
            ============================================= -->
            <div id="details" class="section m-0"
                 style="padding: 120px 0; background: #FFF url('/static/xsite_template/all_templates/xsite_template_seven/images/instructor.jpg') no-repeat left top / cover">
                <div class="container">
                    <div class="row">

                        <div class="col-md-7"></div>

                        <div class="col-md-5">
                            <div class="heading-block nobottomborder mb-4 mt-5">
                                <h3 id="other_details_title">More To Know Us</h3>
                            </div>
                            <p class="mb-2" id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit
                                voluptatem
                                accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                                veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam
                                voluptatem quia
                                voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui
                                ratione
                                voluptatem sequi nesciunt?</p>
                        </div>

                    </div>
                </div>
            </div>

            <div class="promo promo-light promo-full footer-stick" style="padding: 30px 0 !important;">
                <div class="container clearfix">
                    <h3 class="ls-1 ">Call us today at <span style="color: orange;" class="phone">03334455667</span> or
                        Email us
                        at
                        <span style="color: orange;" class="email">support@gmail.com</span></h3>
                    <!-- <span class="text-black-50">We strive to provide Our Customers with Top Notch Support to make their Theme Experience Wonderful.</span> -->
                    <a href="#Form_page"
                       class="button button-xlarge button-rounded nott ls0 t400  bg-Carrot banner_button_text">Get your
                        ebook</a>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="dark">
        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="pt-2 pb-2">

            <div class="container clearfix">

                <div class="row align-items-center justify-content-between">
                    <div class="col-md-6">
                        &copy; 2020 <strong><a href="https://prospectx.com/"
                                               target="_blank" style="color: orange;">Prospectx</a></strong> All Rights
                        Reserved.<br>
                    </div>
                </div>

            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->
</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="icon-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>
</body>"""

    Vacation_head = """<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta name="author" content="SemiColonWeb"/>

    <!-- Stylesheets
    ============================================= -->
    <link href="http://fonts.googleapis.com/css?family=Istok+Web:400,700" rel="stylesheet" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/bootstrap.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/style.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/dark.css" type="text/css"/>

    <!-- Pet Demo Specific Stylesheet -->
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_eight/css/fonts.css"
          type="text/css"/>

    <link rel="stylesheet" href="/static/xsite_template/css/font-icons.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/animate.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/css/magnific-popup.css" type="text/css"/>


    <link rel="stylesheet" href="/static/xsite_template/css/responsive.css" type="text/css"/>
    <link rel="stylesheet" href="/static/xsite_template/all_templates/xsite_template_eight/template_eight.css"
          type="text/css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <script src="http://css3-mediaqueries-js.googlecode.com/svn/trunk/css3-mediaqueries.js"></script>
    <link rel="stylesheet" href="/static/xsite_template/css/colors.php?color=f0a540" type="text/css"/>
<link rel="stylesheet" href="/static/plugins/fontawesome-free-5.13.0-web/css/all.css">

    <!-- Document Title
    ============================================= -->
    <title>Xsite</title>
</head>"""
    Vacation_body = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <!-- Header
    ============================================= -->
    <header id="header" class="transparent-header " data-sticky-class="not-dark">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo"
                       data-dark-logo="/media/xsite_images/website_logos/prospectx-logo.png"><img class="logo_img"
                                                                                                src="/media/xsite_images/website_logos/prospectx-logo.png"
                                                                                                alt="Logo "></a>
                    <a href="#" class="retina-logo"
                       data-dark-logo="/media/xsite_images/website_logos/prospectx-logo.png"><img class="logo_img"
                                                                                                src="/media/xsite_images/website_logos/prospectx-logo.png"
                                                                                                alt="Logo" width="60%"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu" class="not-dark">

                    <ul>
                        <li><a class="template_eight_nav" href="#home">
                            <div>Home</div>
                        </a></li>
                        <li><a class="template_eight_nav" href="#about">
                            <div>About</div>
                        </a></li>
                        <li><a class="template_eight_nav" href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                        <li><a class="template_eight_nav" href="#more_detail">
                            <div>Detail</div>
                        </a></li>
                        <li class="bgcolor get_a_qoute "><a href="#get_a_qoute" style="background: #1ABC9C;">
                            <div class="banner_button_text">Get Your Ebook</div>
                        </a></li>
                    </ul>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="home" class="slider-element full-screen clearfix"
             style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/banner.jpg') center right no-repeat; background-size: cover;">
        <div class="vertical-middle">
            <div class="container clearfix">

                <div class="emphasis-title dark mt-3 text-center template_eight_banner">
                    <h2 id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home Prices.</h2><br>
                    <a href="#get_a_qoute"
                       class="button button-large button-rounded noleftmargin banner_button_text">Get your ebook</a>
                </div>

            </div>
        </div>
    </section>

    <!-- About
    ============================================= -->
    <section id="about">

        <div class="content-wrap notoppadding clearfix pb-0">

            <div class="section nomargin clearfix" style="background-color: #eef2f5;">
                <div class="container clearfix">

                    <div class="heading-block center nobottomborder bottommargin topmargin-sm divcenter"
                         style="max-width: 940px">
                        <h3 class="nott font-secondary t400"
                            style="font-size: 36px;" id="about_us_title">Little More Detail About Us</h3>
                        <span id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</span>

                    </div>

                </div>
            </div>
            <div class="container topmargin pt-4 pb-4 clearfix" id="testimonials">
                <div class="row clearfix pt-1">
                    <div class="col-lg-7">
                        <div class="heading-block nobottomborder topmargin-sm nobottommargin">
                            <h2 class="font-secondary ls1 nott t400">Testimonials</h2>
                            <span>We give FAIR cash offers for your home! Give us a call today or fill out one of the forms on our website!</span>
                            <a href="#get_a_qoute"
                               class="button button-large button-rounded topmargin-sm noleftmargin banner_button_text">Get
                                Your ebook</a>
                            <div class="line line-sm"></div>
                        </div>
                        <div class="row clearfix">
                            <div class="col-md-4">
                                <div>
                                    <div class="counter counter-small color"><span data-from="10" data-to="1136"
                                                                                   data-refresh-interval="50"
                                                                                   data-speed="1000"></span>+
                                    </div>
                                    <h5 class="color t600 nott notopmargin" style="font-size: 16px;">Happy Customers
                                    </h5>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <div>
                                    <div class="counter counter-small" style="color: #22c1c3;"><span data-from="10"
                                                                                                     data-to="145"
                                                                                                     data-refresh-interval="50"
                                                                                                     data-speed="700"></span>+
                                    </div>
                                    <h5 class="t600 nott notopmargin" style="color: #22c1c3; font-size: 16px;">
                                        Property Sold</h5>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <div>
                                    <div class="counter counter-small" style="color: #BD3F32;"><span data-from="10"
                                                                                                     data-to="50"
                                                                                                     data-refresh-interval="85"
                                                                                                     data-speed="1200"></span>+
                                    </div>
                                    <h5 class="t600 nott notopmargin" style="color: #BD3F32; font-size: 16px;">
                                        Professional builders</h5>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-5 pb-4">
                        <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget"
                             data-nav="false" data-animate-in="slideInUp" data-animate-out="slideOutUp"
                             data-autoplay="5000" data-loop="true" data-stage-padding="5" data-margin="10"
                             data-items-sm="1" data-items-md="1" data-items-xl="1">

                            <div class="oc-item">
                                <div class="testimonial topmargin-sm">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/1.jpg"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit
                                            voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_1_person_name">Person 1</span>
                                            <span id="testi_1_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="oc-item">

                                <div class="testimonial topmargin-sm">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/2.jpg"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit
                                            voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_2_person_name">Person 1</span>
                                            <span id="testi_2_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>

                            </div>
                            <div class="oc-item">

                                <div class="testimonial topmargin-sm">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/3.jpg"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit
                                            voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_3_person_name">Person 1</span>
                                            <span id="testi_3_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>


            <div class="section nomargin  clearfix" id="more_detail">
                <div class="container clearfix">
                    <div class="row topmargin clearfix">
                        <div class="col-lg-5 d-none d-lg-block">
                            <img src="/static/xsite_template/all_templates/xsite_template_eight/images/banner1.jpg"
                                 alt="">
                        </div>
                        <div class="col-lg-7 col-md-12">
                            <div class="heading-block  nobottomborder divcenter" style="max-width: 640px">
                                <h3 class="nott font-secondary t400"
                                    style="font-size: 36px;" id="other_details_title">More To Know Us</h3>
                                <span id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
									</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="section nobottommargin nobg clearfix" style="background-color: #eef2f5;" id="get_a_qoute">
                <div class="container">

                    <div class="row">
                        <div class="col-md-7">
                            <div class="heading-block  nobottomborder nobottommargin divcenter"
                                 style="max-width: 640px">
                                <h3 class="nott font-secondary t400 banner_button_text"
                                    style="font-size: 36px;">Get your button</h3>
                                <span>We never say no to a home that is not in a perfect condition. We buy all types of houses to help you close quickly and get the most money for your home!</span>
                            </div>
                        </div>

                        <div class="col-md-5 ">
                            <div class="widget mt-4 form-widget clearfix">
                                <h4 id="banner_title1">Find Your Dream Home Here! Beautiful Homes At Ugly Home
                                    Prices.</h4>
                                <div class="form-result"></div>
                                <form id="buyer_form" name="quick-contact-form"
                                      method="post" class="quick-contact-form nobottommargin">
                                    <div class="form-process"></div>
                                    <input type="text"
                                           name="fullname"
                                           id="template-contactform-name-buyer" placeholder="Name"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>

                                    <input type="email"
                                           name="email"
                                           id="template-contactform-email-buyer" placeholder="Email"
                                           class="required sm-form-control email input-block-level mb-2"
                                           autocomplete="on"/>

                                    <input type="text" id="template-contactform-phone-buyer"
                                           name="phone" placeholder="Phone"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>

                                    <select id="template-contactform-service-buyer"
                                            name="what_are_you_looking_for"
                                            class="required sm-form-control input-block-level mb-2"
                                            autocomplete="on">
                                        <option value="">What are you looking for?</option>
                                    </select>

                                    <input type="hidden" name="audience" value="Buyer">

                                    <button class="button button-large button-rounded topmargin-xs noleftmargin"
                                            type="submit" id="template-contactform-submit-buyer"
                                            name="template-contactform-submit"
                                            value="submit">Get your ebook
                                    </button>


                                </form>
                                <form id="seller_form" name="quick-contact-form"
                                      method="post" class="quick-contact-form nobottommargin">
                                    <div class="form-process"></div>
                                    <input type="hidden" name="audience" value="Seller">
                                    <input type="text" id="template-contactform-name-seller"
                                           name="fullname" placeholder="Name"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>
                                    <input type="text" id="template-contactform-phone-seller"
                                           name="phone" placeholder="Phone"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>

                                    <input type="email" id="template-contactform-email-seller"
                                           name="email" placeholder="Email"
                                           class="required sm-form-control email input-block-level mb-2"
                                           autocomplete="on"/>

                                    <div class="form-check mb-1">
                                        <label class="form-check-label">

                                            <input name="immediate_assistance" id="immediate_assistance"
                                                   type="checkbox"
                                                   class="form-check-input"
                                                   onclick="javascript:ShowFields()">
                                            I would like immediate assistance
                                        </label>
                                    </div>

                                    <div id="immediate_assistance_fields" style="display: none">
                                        <input type="text" id="template-contactform-address-seller"
                                               name="street_address" placeholder="Street Address"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"/>
                                        <input type="text" id="template-contactform-city-seller"
                                               name="city" placeholder="City"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"/>
                                        <select id="template-contactform-state-seller" name="state"
                                                class="sm-form-control input-block-level mb-2"
                                                autocomplete="on">
                                            <option value="">State</option>
                                            <option value="AL">
                                                Alabama
                                            </option>
                                            <option value="AK">
                                                Alaska
                                            </option>
                                            <option value="AB">
                                                Alberta
                                            </option>
                                            <option value="AS">
                                                American Samoa
                                            </option>
                                            <option value="AZ">
                                                Arizona
                                            </option>
                                            <option value="AR">
                                                Arkansas
                                            </option>
                                            <option value="BC">
                                                British Columbia
                                            </option>
                                            <option value="CA">
                                                California
                                            </option>
                                            <option value="CO">
                                                Colorado
                                            </option>
                                            <option value="CT">
                                                Connecticut
                                            </option>
                                            <option value="DE">
                                                Delaware
                                            </option>
                                            <option value="FM">
                                                Fed. St. of Micronesia
                                            </option>
                                            <option value="FL">
                                                Florida
                                            </option>
                                            <option value="GA">
                                                Georgia
                                            </option>
                                            <option value="GU">
                                                Guam
                                            </option>
                                            <option value="HI">
                                                Hawaii
                                            </option>
                                            <option value="ID">
                                                Idaho
                                            </option>
                                            <option value="IL">
                                                Illinois
                                            </option>
                                            <option value="IN">
                                                Indiana
                                            </option>
                                            <option value="IA">
                                                Iowa
                                            </option>
                                            <option value="KS">
                                                Kansas
                                            </option>
                                            <option value="KY">
                                                Kentucky
                                            </option>
                                            <option value="LA">
                                                Louisiana
                                            </option>
                                            <option value="ME">
                                                Maine
                                            </option>
                                            <option value="MB">
                                                Manitoba
                                            </option>
                                            <option value="MH">
                                                Marshall Islands
                                            </option>
                                            <option value="MD">
                                                Maryland
                                            </option>
                                            <option value="MA">
                                                Massachusetts
                                            </option>
                                            <option value="MI">
                                                Michigan
                                            </option>
                                            <option value="MN">
                                                Minnesota
                                            </option>
                                            <option value="MS">
                                                Mississippi
                                            </option>
                                            <option value="MO">
                                                Missouri
                                            </option>
                                            <option value="MT">
                                                Montana
                                            </option>
                                            <option value="NE">
                                                Nebraska
                                            </option>
                                            <option value="NV">
                                                Nevada
                                            </option>
                                            <option value="NB">
                                                New Brunswick
                                            </option>
                                            <option value="NH">
                                                New Hampshire
                                            </option>
                                            <option value="NJ">
                                                New Jersey
                                            </option>
                                            <option value="NM">
                                                New Mexico
                                            </option>
                                            <option value="NY">
                                                New York
                                            </option>
                                            <option value="NL">
                                                Newfoundland
                                            </option>
                                            <option value="NC">
                                                North Carolina
                                            </option>
                                            <option value="ND">
                                                North Dakota
                                            </option>
                                            <option value="MP">
                                                Northern Mariana Islands
                                            </option>
                                            <option value="NT">
                                                Northwest Territory
                                            </option>
                                            <option value="NS">
                                                Nova Scotia
                                            </option>
                                            <option value="NU">
                                                Nunavut
                                            </option>
                                            <option value="OH">
                                                Ohio
                                            </option>
                                            <option value="OK">
                                                Oklahoma
                                            </option>
                                            <option value="ON">
                                                Ontario
                                            </option>
                                            <option value="OR">
                                                Oregon
                                            </option>
                                            <option value="PA">
                                                Pennsylvania
                                            </option>
                                            <option value="PE">
                                                Prince Edward Island
                                            </option>
                                            <option value="PR">
                                                Puerto Rico
                                            </option>
                                            <option value="QC">
                                                Quebec
                                            </option>
                                            <option value="RI">
                                                Rhode Island
                                            </option>
                                            <option value="SK">
                                                Saskatchewan
                                            </option>
                                            <option value="SC">
                                                South Carolina
                                            </option>
                                            <option value="SD">
                                                South Dakota
                                            </option>
                                            <option value="TN">
                                                Tennessee
                                            </option>
                                            <option value="TX">
                                                Texas
                                            </option>
                                            <option value="UT">
                                                Utah
                                            </option>
                                            <option value="VT">
                                                Vermont
                                            </option>
                                            <option value="VI">
                                                Virgin Islands
                                            </option>
                                            <option value="VA">
                                                Virginia
                                            </option>
                                            <option value="WA">
                                                Washington
                                            </option>
                                            <option value="DC">
                                                Washington DC
                                            </option>
                                            <option value="WV">
                                                West Virginia
                                            </option>
                                            <option value="WI">
                                                Wisconsin
                                            </option>
                                            <option value="WY">
                                                Wyoming
                                            </option>
                                            <option value="YT">
                                                Yukon Territory
                                            </option>
                                        </select>

                                        <input type="text" id="template-contactform-zip-seller"
                                               name="zip" placeholder="Zip"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"/>

                                        <select id="template-contactform-is_home_listed-seller"
                                                name="is_home_listed"
                                                class="sm-form-control input-block-level mb-2"
                                                autocomplete="on">
                                            <option value="">Is home listed?</option>
                                        </select>
                                        <input type="number" id="template-contactform-asking_price-seller"
                                               name="asking_price" placeholder="Asking Price"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"
                                               min="0"/>
                                    </div>

                                    <button class="button button-large button-rounded topmargin-xs noleftmargin"
                                            type="submit" id="template-contactform-seller"
                                            name="template-contactform-submit"
                                            value="submit">Get your ebook
                                    </button>

                                </form>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div class="need_help_section section nobg topmargin-lg nobottommargin  clearfix"
                 style="background-color: #eef2f5 !important;">
                <div class="container ">

                    <div class="heading-block center nobottomborder divcenter" style="max-width: 640px">
                        <h3 class="nott font-secondary t400" style="font-size: 36px;">Need Help?</h3>
                        <span id="call_to_action_text">Nothing here</span>
                    </div>
                    <div class="row contact-properties clearfix">
                        <div id="address_div" class="col-md-4">
                            <a href="#"
                               style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/blocks.jpg') no-repeat center center; background-size: cover;">
                                <div class="vertical-middle dark center">
                                    <div class="heading-block nomargin noborder">
                                        <h3 class="capitalize t400 font-secondary">Visit Us</h3>
                                        <span style="margin-top: 100px; font-size: 17px; font-weight: 500;">
                                            <span id="address">795 Folsom Ave, Suite 600</span><br>
                                            <span id="location">San Francisco, CA 94107</span>
											</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <div id="no_address_div" class="col-md-2"></div>
                        <div class="col-md-4">
                            <a href="#"
                               style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/blocks.jpg') no-repeat center center; background-size: cover;">
                                <div class="vertical-middle dark center">
                                    <div class="heading-block nomargin noborder">
                                        <h3 class="capitalize t400 font-secondary">Make an appiontment</h3>
                                        <span style="margin-top: 100px; font-size: 17px; font-weight: 500;">
												call us<br>
												<span id="phone">03334455667</span>
											</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <div class="col-md-4">
                            <a href="#get_a_qoute"
                               style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/blocks.jpg') no-repeat center center; background-size: cover;">
                                <div class="vertical-middle dark center">
                                    <div class="heading-block nomargin noborder">
                                        <h3 class="capitalize t400 font-secondary banner_button_text">Get your
                                            ebook</h3>
                                        <span style="margin-top: 100px; font-size: 17px; font-weight: 500;">
												Email us<br>
                                            <span id="email">support@gmail.com</span>
											</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="dark">


        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="pb-1 pt-1">

            <div class="container clearfix">

                <div class="col_half text-white mt-2">
                    &copy; 2020 All Rights Reserved by <a href="https://prospectx.com/" target="_blank">Prospectx</a>.
                </div>

                <div class="col_half col_last tright mt-1">
                    <div class="fright clearfix">
                        <a href="#" class="social-icon si-small si-facebook">
                            <i class="fab fa-facebook-f"></i>
                            <i class="fab fa-facebook-f"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-twitter">
                            <i class="fab fa-twitter"></i>
                            <i class="fab fa-twitter"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-gplus">
                            <i class="fab fa-google-plus-g"></i>
                            <i class="fab fa-google-plus-g"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-pinterest">
                            <i class="fab fa-pinterest"></i>
                            <i class="fab fa-pinterest"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-linkedin">
                            <i class="fab fa-linkedin"></i>
                            <i class="fab fa-linkedin"></i>
                        </a>
                    </div>
                </div>

            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->


</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>
</body>"""

    Vacation_body_seller = """<body class="stretched">

<!-- Document Wrapper
============================================= -->
<div id="wrapper" class="clearfix">

    <!-- Header
    ============================================= -->
    <header id="header" class="transparent-header " data-sticky-class="not-dark">

        <div id="header-wrap">

            <div class="container clearfix">

                <div id="primary-menu-trigger"><i class="fa fa-bars"></i></div>

                <!-- Logo
                ============================================= -->
                <div id="logo">
                    <a href="#" class="standard-logo"
                       data-dark-logo="/media/xsite_images/website_logos/prospectx-logo.png"><img class="logo_img"
                                                                                                src="/media/xsite_images/website_logos/prospectx-logo.png"
                                                                                                alt="Logo "></a>
                    <a href="#" class="retina-logo"
                       data-dark-logo="/media/xsite_images/website_logos/prospectx-logo.png"><img class="logo_img"
                                                                                                src="/media/xsite_images/website_logos/prospectx-logo.png"
                                                                                                alt="Logo" width="60%"></a>
                </div><!-- #logo end -->

                <!-- Primary Navigation
                ============================================= -->
                <nav id="primary-menu" class="not-dark">

                    <ul>
                        <li><a class="template_eight_nav" href="#home">
                            <div>Home</div>
                        </a></li>
                        <li><a class="template_eight_nav" href="#about">
                            <div>About</div>
                        </a></li>
                        <li><a class="template_eight_nav" href="#testimonials">
                            <div>Testimonials</div>
                        </a></li>
                        <li><a class="template_eight_nav" href="#more_detail">
                            <div>Detail</div>
                        </a></li>
                        <li class="bgcolor get_a_qoute "><a href="#get_a_qoute" style="background: #1ABC9C;">
                            <div class="banner_button_text">Get Your Ebook</div>
                        </a></li>
                    </ul>

                </nav><!-- #primary-menu end -->

            </div>

        </div>

    </header><!-- #header end -->

    <!-- Slider
    ============================================= -->
    <section id="home" class="slider-element full-screen clearfix"
             style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/banner.jpg') center right no-repeat; background-size: cover;">
        <div class="vertical-middle">
            <div class="container clearfix">

                <div class="emphasis-title dark mt-3 text-center template_eight_banner">
                    <h2 id="banner_title">Find Your Dream Home Here! Beautiful Homes At Ugly Home Prices.</h2><br>
                    <a href="#get_a_qoute"
                       class="button button-large button-rounded noleftmargin banner_button_text">Get your ebook</a>
                </div>

            </div>
        </div>
    </section>

    <!-- About
    ============================================= -->
    <section id="about">

        <div class="content-wrap notoppadding clearfix pb-0">

            <div class="section nomargin clearfix" style="background-color: #eef2f5;">
                <div class="container clearfix">

                    <div class="heading-block center nobottomborder bottommargin topmargin-sm divcenter"
                         style="max-width: 940px">
                        <h3 class="nott font-secondary t400"
                            style="font-size: 36px;" id="about_us_title">Little More Detail About Us</h3>
                        <span id="about_us_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
                        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi
                        architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
                        aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
                        sequi nesciunt?</span>

                    </div>

                </div>
            </div>
            <div class="container topmargin pt-4 pb-4 clearfix" id="testimonials">
                <div class="row clearfix pt-1">
                    <div class="col-lg-7">
                        <div class="heading-block nobottomborder topmargin-sm nobottommargin">
                            <h2 class="font-secondary ls1 nott t400">Testimonials</h2>
                            <span>Get Deals First hand!! Give us a call today or fill out one of the forms on our website!</span>
                            <a href="#get_a_qoute"
                               class="button button-large button-rounded topmargin-sm noleftmargin banner_button_text">Get
                                Your ebook</a>
                            <div class="line line-sm"></div>
                        </div>
                        <div class="row clearfix">
                            <div class="col-md-4">
                                <div>
                                    <div class="counter counter-small color"><span data-from="10" data-to="1136"
                                                                                   data-refresh-interval="50"
                                                                                   data-speed="1000"></span>+
                                    </div>
                                    <h5 class="color t600 nott notopmargin" style="font-size: 16px;">Happy Customers
                                    </h5>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <div>
                                    <div class="counter counter-small" style="color: #22c1c3;"><span data-from="10"
                                                                                                     data-to="145"
                                                                                                     data-refresh-interval="50"
                                                                                                     data-speed="700"></span>+
                                    </div>
                                    <h5 class="t600 nott notopmargin" style="color: #22c1c3; font-size: 16px;">
                                        Property Deals</h5>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <div>
                                    <div class="counter counter-small" style="color: #BD3F32;"><span data-from="10"
                                                                                                     data-to="50"
                                                                                                     data-refresh-interval="85"
                                                                                                     data-speed="1200"></span>+
                                    </div>
                                    <h5 class="t600 nott notopmargin" style="color: #BD3F32; font-size: 16px;">
                                        Professional builders</h5>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-5 pb-4">
                        <div id="oc-testi" class="oc-testi owl-carousel testimonials-carousel carousel-widget"
                             data-nav="false" data-animate-in="slideInUp" data-animate-out="slideOutUp"
                             data-autoplay="5000" data-loop="true" data-stage-padding="5" data-margin="10"
                             data-items-sm="1" data-items-md="1" data-items-xl="1">

                            <div class="oc-item">
                                <div class="testimonial topmargin-sm">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/1.jpg"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_1_text">Sed ut perspiciatis unde omnis iste natus error sit
                                            voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_1_person_name">Person 1</span>
                                            <span id="testi_1_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="oc-item">

                                <div class="testimonial topmargin-sm">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/2.jpg"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_2_text">Sed ut perspiciatis unde omnis iste natus error sit
                                            voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_2_person_name">Person 1</span>
                                            <span id="testi_2_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>

                            </div>
                            <div class="oc-item">

                                <div class="testimonial topmargin-sm">
                                    <div class="testi-image">
                                        <a href="#"><img
                                                src="/static/xsite_template/all_templates/xsite_template_eight/images/testimonials/3.jpg"
                                                alt="Customer Testimonails"></a>
                                    </div>
                                    <div class="testi-content">
                                        <p id="testi_3_text">Sed ut perspiciatis unde omnis iste natus error sit
                                            voluptatem
                                            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab
                                            illo
                                            inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                                            Nemo enim
                                            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                                            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt?</p>
                                        <div class="testi-meta">
                                            <span id="testi_3_person_name">Person 1</span>
                                            <span id="testi_3_company_name">Argon Tech</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>


            <div class="section nomargin  clearfix" id="more_detail">
                <div class="container clearfix">
                    <div class="row topmargin clearfix">
                        <div class="col-lg-5 d-none d-lg-block">
                            <img src="/static/xsite_template/all_templates/xsite_template_eight/images/banner1.jpg"
                                 alt="">
                        </div>
                        <div class="col-lg-7 col-md-12">
                            <div class="heading-block  nobottomborder divcenter" style="max-width: 640px">
                                <h3 class="nott font-secondary t400"
                                    style="font-size: 36px;" id="other_details_title">More To Know Us</h3>
                                <span id="other_details_desc">Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
                        veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                        voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
                        voluptatem sequi nesciunt?
									</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="section nobottommargin nobg clearfix" style="background-color: #eef2f5;" id="get_a_qoute">
                <div class="container">

                    <div class="row">
                        <div class="col-md-7">
                            <div class="heading-block  nobottomborder nobottommargin divcenter"
                                 style="max-width: 640px">
                                <h3 class="nott font-secondary t400 banner_button_text"
                                    style="font-size: 36px;">Get your button</h3>
                                <span>We never say no to a home that is not in a perfect condition. We buy all types of houses to help you close quickly and get the most money for your home!</span>
                            </div>
                        </div>

                        <div class="col-md-5 ">
                            <div class="widget mt-4 form-widget clearfix">
                                <h4 id="banner_title1">Find Your Dream Home Here! Beautiful Homes At Ugly Home
                                    Prices.</h4>
                                <div class="form-result"></div>
                                <form id="buyer_form" name="quick-contact-form"
                                      method="post" class="quick-contact-form nobottommargin">
                                    <div class="form-process"></div>
                                    <input type="text"
                                           name="fullname"
                                           id="template-contactform-name-buyer" placeholder="Name"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>

                                    <input type="email"
                                           name="email"
                                           id="template-contactform-email-buyer" placeholder="Email"
                                           class="required sm-form-control email input-block-level mb-2"
                                           autocomplete="on"/>

                                    <input type="text" id="template-contactform-phone-buyer"
                                           name="phone" placeholder="Phone"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>

                                    <select id="template-contactform-service-buyer"
                                            name="what_are_you_looking_for"
                                            class="required sm-form-control input-block-level mb-2"
                                            autocomplete="on">
                                        <option value="">What are you looking for?</option>
                                    </select>

                                    <input type="hidden" name="audience" value="Buyer">

                                    <button class="button button-large button-rounded topmargin-xs noleftmargin"
                                            type="submit" id="template-contactform-submit-buyer"
                                            name="template-contactform-submit"
                                            value="submit">Get your ebook
                                    </button>


                                </form>
                                <form id="seller_form" name="quick-contact-form"
                                      method="post" class="quick-contact-form nobottommargin">
                                    <div class="form-process"></div>
                                    <input type="hidden" name="audience" value="Seller">
                                    <input type="text" id="template-contactform-name-seller"
                                           name="fullname" placeholder="Name"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>
                                    <input type="text" id="template-contactform-phone-seller"
                                           name="phone" placeholder="Phone"
                                           class="required sm-form-control input-block-level mb-2"
                                           autocomplete="on"/>

                                    <input type="email" id="template-contactform-email-seller"
                                           name="email" placeholder="Email"
                                           class="required sm-form-control email input-block-level mb-2"
                                           autocomplete="on"/>

                                    <div class="form-check mb-1">
                                        <label class="form-check-label">

                                            <input name="immediate_assistance" id="immediate_assistance"
                                                   type="checkbox"
                                                   class="form-check-input"
                                                   onclick="javascript:ShowFields()">
                                            I would like immediate assistance
                                        </label>
                                    </div>

                                    <div id="immediate_assistance_fields" style="display: none">
                                        <input type="text" id="template-contactform-address-seller"
                                               name="street_address" placeholder="Street Address"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"/>
                                        <input type="text" id="template-contactform-city-seller"
                                               name="city" placeholder="City"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"/>
                                        <select id="template-contactform-state-seller" name="state"
                                                class="sm-form-control input-block-level mb-2"
                                                autocomplete="on">
                                            <option value="">State</option>
                                            <option value="AL">
                                                Alabama
                                            </option>
                                            <option value="AK">
                                                Alaska
                                            </option>
                                            <option value="AB">
                                                Alberta
                                            </option>
                                            <option value="AS">
                                                American Samoa
                                            </option>
                                            <option value="AZ">
                                                Arizona
                                            </option>
                                            <option value="AR">
                                                Arkansas
                                            </option>
                                            <option value="BC">
                                                British Columbia
                                            </option>
                                            <option value="CA">
                                                California
                                            </option>
                                            <option value="CO">
                                                Colorado
                                            </option>
                                            <option value="CT">
                                                Connecticut
                                            </option>
                                            <option value="DE">
                                                Delaware
                                            </option>
                                            <option value="FM">
                                                Fed. St. of Micronesia
                                            </option>
                                            <option value="FL">
                                                Florida
                                            </option>
                                            <option value="GA">
                                                Georgia
                                            </option>
                                            <option value="GU">
                                                Guam
                                            </option>
                                            <option value="HI">
                                                Hawaii
                                            </option>
                                            <option value="ID">
                                                Idaho
                                            </option>
                                            <option value="IL">
                                                Illinois
                                            </option>
                                            <option value="IN">
                                                Indiana
                                            </option>
                                            <option value="IA">
                                                Iowa
                                            </option>
                                            <option value="KS">
                                                Kansas
                                            </option>
                                            <option value="KY">
                                                Kentucky
                                            </option>
                                            <option value="LA">
                                                Louisiana
                                            </option>
                                            <option value="ME">
                                                Maine
                                            </option>
                                            <option value="MB">
                                                Manitoba
                                            </option>
                                            <option value="MH">
                                                Marshall Islands
                                            </option>
                                            <option value="MD">
                                                Maryland
                                            </option>
                                            <option value="MA">
                                                Massachusetts
                                            </option>
                                            <option value="MI">
                                                Michigan
                                            </option>
                                            <option value="MN">
                                                Minnesota
                                            </option>
                                            <option value="MS">
                                                Mississippi
                                            </option>
                                            <option value="MO">
                                                Missouri
                                            </option>
                                            <option value="MT">
                                                Montana
                                            </option>
                                            <option value="NE">
                                                Nebraska
                                            </option>
                                            <option value="NV">
                                                Nevada
                                            </option>
                                            <option value="NB">
                                                New Brunswick
                                            </option>
                                            <option value="NH">
                                                New Hampshire
                                            </option>
                                            <option value="NJ">
                                                New Jersey
                                            </option>
                                            <option value="NM">
                                                New Mexico
                                            </option>
                                            <option value="NY">
                                                New York
                                            </option>
                                            <option value="NL">
                                                Newfoundland
                                            </option>
                                            <option value="NC">
                                                North Carolina
                                            </option>
                                            <option value="ND">
                                                North Dakota
                                            </option>
                                            <option value="MP">
                                                Northern Mariana Islands
                                            </option>
                                            <option value="NT">
                                                Northwest Territory
                                            </option>
                                            <option value="NS">
                                                Nova Scotia
                                            </option>
                                            <option value="NU">
                                                Nunavut
                                            </option>
                                            <option value="OH">
                                                Ohio
                                            </option>
                                            <option value="OK">
                                                Oklahoma
                                            </option>
                                            <option value="ON">
                                                Ontario
                                            </option>
                                            <option value="OR">
                                                Oregon
                                            </option>
                                            <option value="PA">
                                                Pennsylvania
                                            </option>
                                            <option value="PE">
                                                Prince Edward Island
                                            </option>
                                            <option value="PR">
                                                Puerto Rico
                                            </option>
                                            <option value="QC">
                                                Quebec
                                            </option>
                                            <option value="RI">
                                                Rhode Island
                                            </option>
                                            <option value="SK">
                                                Saskatchewan
                                            </option>
                                            <option value="SC">
                                                South Carolina
                                            </option>
                                            <option value="SD">
                                                South Dakota
                                            </option>
                                            <option value="TN">
                                                Tennessee
                                            </option>
                                            <option value="TX">
                                                Texas
                                            </option>
                                            <option value="UT">
                                                Utah
                                            </option>
                                            <option value="VT">
                                                Vermont
                                            </option>
                                            <option value="VI">
                                                Virgin Islands
                                            </option>
                                            <option value="VA">
                                                Virginia
                                            </option>
                                            <option value="WA">
                                                Washington
                                            </option>
                                            <option value="DC">
                                                Washington DC
                                            </option>
                                            <option value="WV">
                                                West Virginia
                                            </option>
                                            <option value="WI">
                                                Wisconsin
                                            </option>
                                            <option value="WY">
                                                Wyoming
                                            </option>
                                            <option value="YT">
                                                Yukon Territory
                                            </option>
                                        </select>

                                        <input type="text" id="template-contactform-zip-seller"
                                               name="zip" placeholder="Zip"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"/>

                                        <select id="template-contactform-is_home_listed-seller"
                                                name="is_home_listed"
                                                class="sm-form-control input-block-level mb-2"
                                                autocomplete="on">
                                            <option value="">Is home listed?</option>
                                        </select>
                                        <input type="number" id="template-contactform-asking_price-seller"
                                               name="asking_price" placeholder="Asking Price"
                                               class="sm-form-control input-block-level mb-2"
                                               autocomplete="on"
                                               min="0"/>
                                    </div>

                                    <button class="button button-large button-rounded topmargin-xs noleftmargin"
                                            type="submit" id="template-contactform-seller"
                                            name="template-contactform-submit"
                                            value="submit">Get your ebook
                                    </button>

                                </form>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div class="need_help_section section nobg topmargin-lg nobottommargin  clearfix"
                 style="background-color: #eef2f5 !important;">
                <div class="container ">

                    <div class="heading-block center nobottomborder divcenter" style="max-width: 640px">
                        <h3 class="nott font-secondary t400" style="font-size: 36px;">Need Help?</h3>
                        <span id="call_to_action_text">Nothing here</span>
                    </div>
                    <div class="row contact-properties clearfix">
                        <div id="address_div" class="col-md-4">
                            <a href="#"
                               style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/blocks.jpg') no-repeat center center; background-size: cover;">
                                <div class="vertical-middle dark center">
                                    <div class="heading-block nomargin noborder">
                                        <h3 class="capitalize t400 font-secondary">Visit Us</h3>
                                        <span style="margin-top: 100px; font-size: 17px; font-weight: 500;">
                                            <span id="address">795 Folsom Ave, Suite 600</span><br>
                                            <span id="location">San Francisco, CA 94107</span>
											</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <div id="no_address_div" class="col-md-2"></div>
                        <div class="col-md-4">
                            <a href="#"
                               style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/blocks.jpg') no-repeat center center; background-size: cover;">
                                <div class="vertical-middle dark center">
                                    <div class="heading-block nomargin noborder">
                                        <h3 class="capitalize t400 font-secondary">Make an appiontment</h3>
                                        <span style="margin-top: 100px; font-size: 17px; font-weight: 500;">
												call us<br>
												<span id="phone">03334455667</span>
											</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <div class="col-md-4">
                            <a href="#get_a_qoute"
                               style="background: url('/static/xsite_template/all_templates/xsite_template_eight/images/blocks.jpg') no-repeat center center; background-size: cover;">
                                <div class="vertical-middle dark center">
                                    <div class="heading-block nomargin noborder">
                                        <h3 class="capitalize t400 font-secondary banner_button_text">Get your
                                            ebook</h3>
                                        <span style="margin-top: 100px; font-size: 17px; font-weight: 500;">
												Email us<br>
                                            <span id="email">support@gmail.com</span>
											</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </section><!-- #content end -->

    <!-- Footer
    ============================================= -->
    <footer id="footer" class="dark">


        <!-- Copyrights
        ============================================= -->
        <div id="copyrights" class="pb-1 pt-1">

            <div class="container clearfix">

                <div class="col_half text-white mt-2">
                    &copy; 2020 All Rights Reserved by <a href="https://prospectx.com/" target="_blank">Prospectx</a>.
                </div>

                <div class="col_half col_last tright mt-1">
                    <div class="fright clearfix">
                        <a href="#" class="social-icon si-small si-facebook">
                            <i class="fab fa-facebook-f"></i>
                            <i class="fab fa-facebook-f"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-twitter">
                            <i class="fab fa-twitter"></i>
                            <i class="fab fa-twitter"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-gplus">
                            <i class="fab fa-google-plus-g"></i>
                            <i class="fab fa-google-plus-g"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-pinterest">
                            <i class="fab fa-pinterest"></i>
                            <i class="fab fa-pinterest"></i>
                        </a>

                        <a href="#" class="social-icon si-small si-linkedin">
                            <i class="fab fa-linkedin"></i>
                            <i class="fab fa-linkedin"></i>
                        </a>
                    </div>
                </div>

            </div>

        </div><!-- #copyrights end -->

    </footer><!-- #footer end -->


</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="fa fa-angle-up"></div>

<!-- External JavaScripts
============================================= -->
<script src="/static/xsite_template/js/jquery.js"></script>
<script src="/static/xsite_template/js/plugins.js"></script>

<script src="/static/assets/js/jquery.inputmask.bundle.js"></script>

<script>
    $(document).ready(function () {
        $('#template-contactform-phone-buyer').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-phone-seller').focus(function () {
            var mask = "999-999-9999";
            $(this).inputmask(mask, {"placeholder": ""});
        });

        $('#template-contactform-zip-seller').focus(function () {
            var mask = "99999";
            $(this).inputmask(mask, {"placeholder": ""});
        });
    });
</script>
</body>"""

    SiteDesign.objects.create(template_name="XCanvas",
                              template_url="xsite/site_design_templates/xsite_template_1.html",
                              template_image="/Site_Design_imgs/4.jpg",
                              html_head_content=XCanvas_head,
                              html_body_content=XCanvas_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Violet",
                              template_url="xsite/site_design_templates/xsite_template_2.html",
                              template_image="/Site_Design_imgs/1.jpg",
                              html_head_content=Violet_head,
                              html_body_content=Violet_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="XBrownStone",
                              template_url="xsite/site_design_templates/xsite_template_3.html",
                              template_image="/Site_Design_imgs/2.jpg",
                              html_head_content=XBrownStone_head,
                              html_body_content=XBrownStone_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Modernistic",
                              template_url="xsite/site_design_templates/xsite_template_4.html",
                              template_image="/Site_Design_imgs/3.jpg",
                              html_head_content=Modernistic_head,
                              html_body_content=Modernistic_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Dark",
                              template_url="xsite/site_design_templates/xsite_template_5.html",
                              template_image="/Site_Design_imgs/5.png",
                              content_pack=buyer_content_pack,
                              html_head_content=Dark_head,
                              html_body_content=Dark_body,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Business",
                              template_url="xsite/site_design_templates/xsite_template_6.html",
                              template_image="/Site_Design_imgs/6.png",
                              html_head_content=Business_head,
                              html_body_content=Business_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Educational",
                              template_url="xsite/site_design_templates/xsite_template_7.html",
                              template_image="/Site_Design_imgs/7.png",
                              html_head_content=Educational_head,
                              html_body_content=Educational_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Vacation",
                              template_url="xsite/site_design_templates/xsite_template_8.html",
                              template_image="/Site_Design_imgs/8.png",
                              html_head_content=Vacation_head,
                              html_body_content=Vacation_body,
                              content_pack=buyer_content_pack,
                              audience=audience_buyer,
                              category=category,
                              is_lander_page=True)

    SiteDesign.objects.create(template_name="XCanvas",
                              template_url="xsite/site_design_templates/xsite_template_1.html",
                              template_image="/Site_Design_imgs/4.jpg",
                              html_head_content=XCanvas_head,
                              html_body_content=XCanvas_body,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Violet",
                              template_url="xsite/site_design_templates/xsite_template_2.html",
                              template_image="/Site_Design_imgs/1.jpg",
                              html_head_content=Violet_head,
                              html_body_content=Violet_body,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="XBrownStone",
                              template_url="xsite/site_design_templates/xsite_template_3.html",
                              template_image="/Site_Design_imgs/2.jpg",
                              html_head_content=XBrownStone_head,
                              html_body_content=XBrownStone_body_seller,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Modernistic",
                              template_url="xsite/site_design_templates/xsite_template_4.html",
                              template_image="/Site_Design_imgs/3.jpg",
                              html_head_content=Modernistic_head,
                              html_body_content=Modernistic_body_seller,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Dark",
                              template_url="xsite/site_design_templates/xsite_template_5.html",
                              template_image="/Site_Design_imgs/5.png",
                              html_head_content=Dark_head,
                              html_body_content=Dark_body,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Business",
                              template_url="xsite/site_design_templates/xsite_template_6.html",
                              template_image="/Site_Design_imgs/6.png",
                              html_head_content=Business_head,
                              html_body_content=Business_body_seller,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Educational",
                              template_url="xsite/site_design_templates/xsite_template_7.html",
                              template_image="/Site_Design_imgs/7.png",
                              html_head_content=Educational_head,
                              html_body_content=Educational_body_seller,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)
    SiteDesign.objects.create(template_name="Vacation",
                              template_url="xsite/site_design_templates/xsite_template_8.html",
                              template_image="/Site_Design_imgs/8.png",
                              html_head_content=Vacation_head,
                              html_body_content=Vacation_body_seller,
                              content_pack=seller_content_pack,
                              audience=audience_seller,
                              category=category,
                              is_lander_page=True)


class Migration(migrations.Migration):
    dependencies = [
        ('xsiteApp', '0006_auto_20200521_2051'),
    ]

    operations = [
        migrations.RunPython(xsite_data_migrations),
    ]

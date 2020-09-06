# Visual Bloom Filter

A Bloom filter implementation that uses a Raspberry Pi and a Pimoroni Unicorn Hat to display the status of each of the 64 bits comprising the filter.

This example is written in Python, exposes an API with Flask and uses the murmurhash3 library for hashing functions.

## Ingredients

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) (API framework).
* [Murmur3 hashing](https://pypi.org/project/murmurhash3/) (for hash functions).
* [Bulma](https://bulma.io/) (front end CSS).
* [Pimoroni Unicorn Hat library for Python](http://docs.pimoroni.com/unicornhat/).
* [Pimoroni Unicorn Hat](https://shop.pimoroni.com/products/unicorn-hat) - there is also a more expensive HD version with more pixels if you want a bigger array for your filter!
* [Raspberry Pi Model A+ v1](https://www.raspberrypi.org/products/raspberry-pi-1-model-a-plus/) (any 40 pin GPIO Pi that can take HAT boards will work, which is most of them - the model I used is long obsolete I just had one kicking around).
* [USB wifi dongle for Raspberry Pi](https://www.adafruit.com/product/814) (A doesn't come with built in wifi - other models have this onboard - find these USB dongle on Amazon or eBay just make sure to get one that is known to work with the Pi / Raspbian OS).
* [Adafruit Smoked Plastic Pi case](https://www.adafruit.com/product/2361) - get the separate smoked lid too as this is what acts as a nice LED diffuser.  This is the case for A sized Pi models, they also sell them for the larger Pi models.

## Resources

* [GeeksforGeeks article on Bloom filters in Python](https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/).
* [JavaScript Bloom filter implementation with visualization](https://www.jasondavies.com/bloomfilter/).

## Installation and Setup

Make sure you're using Python 3 (I tested this with 3.8).

```bash
$ git clone https://github.com/simonprickett/visual-bloom-filter-for-pi.git
$ cd visual-bloom-filter-for-pi
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

### Hardware

* Connect the Unicorn hat to all 40 GPIO pins on the Pi.
* Install Raspbian / Raspberry Pi OS and configure it for your wifi, or plug it into a wired network.  Make sure you turn on SSH so you can ssh into the Pi from other computers on your network.
* If, like mine, your Pi needs a wifi dongle, plug that into a USB port and configure as needed.
* Make a note of the Pi's IP address.

### Software

The project has two main components, a backend / API written in Python using [Flask](https://flask.palletsprojects.com/en/1.1.x/), and a front end written in vanilla JavaScript using [Bulma](https://bulma.io/) CSS.  There's no build step required for the JavaScript and nothing to `npm install` :)

#### Flask Application

The Flask application code is all in `app.py`, here's a quick walkthrough:

I start off by defining some constants, initializing Flask and configuring the Unicorn hat so that LED 0, 0 is in the top left hand corner according to the way I have the Raspberry Pi oriented... I then get the size of the Unicorn Hat (Pimoroni make other models that have different sizes and I wanted to make the code pretty generic).

The utility function `get_led_position` translates a number into its equivalent row and column position on the LED matrix for the Unicorn Hat.  So, 10 for example would be row 1, column 1 for an 8 x 8 Unicorn Hat where the rows and columns are both 0 - 7 inclusive.

Function `toggle_leds` TODO...

Function `query_led_status` TODO...

Function `set_led_status` TODO...

Function `add_to_filter` TODO...

Function `exists_in_filter` TODO...

Function `reset_filter` TODO...

TODO Flask routes...

#### JavaScript / Bulma Front End

The front end is a single HTML page (`templates/homepage.html`) that works together with a single JavaScript file `static/app.js`.

The vast majority of the styling comes from Bulma (`static/bulma.min.css`) with a tiny bit of link styling in `static/app.css`.  

Here's how it all works:

TODO

## Starting the Application

Because of the way the Unicorn Hat library accesses the hardware, this needs to run as root, so:

```bash
$ sudo bash
# . venv/bin/activate
# flask run --host=0.0.0.0
```

Be sure to specify `--host=0.0.0.0` when starting Flask, so you can access the front end from other machines on your local network.

## Using the Application's Front End

To get to the application's front end, point your browser at `http://<pi ip address>:5000/`.

Once the page has loaded, you can use the "Add" button to add a new entry to the Bloom filter, "Exists" to see if an entry might be in the Bloom filter and "Reset" to clear all bits in the Bloom filter.

## Using the Application's API

### Add an Element to the Bloom Filter

**Request:**

```bash
$ curl --location --request POST 'http://<pi ip address>:5000/api/add/frederick'
```

**Response:**

```json
{
    "result": true
}
```

Response will always be `true`.  Return code is always 201.  The LEDs will indicate which bits in the Bloom filter your new element hashed to.

### See if an Element Exists in the Bloom Filter

**Request:**

```bash
$ curl --location --request GET 'http://<pi ip address>:5000/api/exists/robert'
```

**Response:**

```json
{
    "result": false
}
```

Remember that this is a **probabalistic** data structure, so a response of `false` means the element is definitely not there, and `true` means it might be there.  Return code is 200.

The LEDs will change color to indicate which bits in the Bloom filter are queried.  This will fail "fast" so the first bit checked and found unset will stop the process and return `false`.

### Reset the Bloom Filter

**Request:**

```bash
$ curl --location --request POST 'http://<pi ip address>:5000/api/reset'
```

**Response:**

```json
{
    "result": true
}
```

Response will always be `true`.  Return code is 200.  All LEDs will flash blue to indicate the Bloom filter has been reset, then all of the LEDs will turn off until you add new elements to the new filter instance.

## Other Notes

This implementation is case sensitive, so "Simon", "SIMON", and "simon" will be considered different entries.

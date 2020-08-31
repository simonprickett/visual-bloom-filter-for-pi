# Visual Bloom Filter

A Bloom filter implementation that uses a Raspberry Pi and a Pimoroni Unicorn Hat to display the status of each of the 64 bits comprising the filter.

This example is written in Python, exposes an API with Flask and uses the murmurhash3 library for hashing functions.

## Ingredients

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) (API framework).
* [Murmur3 hashing](https://pypi.org/project/murmurhash3/) (for hash functions).
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

Response will always be `true`.  Return code is 201.

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

Response will always be `true`.  Return code is 200.

## Other Notes

This implementation is case sensitive, so "Simon", "SIMON", and "simon" will be considered different entries.

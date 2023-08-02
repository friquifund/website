# This file is to locally test the jekyll website inside a docker container, to do so docker is the only
# software dependency you need on your laptop, assuming yo have it, you can then run the following commands from
#the repo root folder:
# docker build --platform=linux/amd64 -t frikiwebsite .
# docker run -p 4000:4000 --platform=linux/amd64 frikiwebsite
# Then go to localhost:4000

# Use a base image with Ruby and Jekyll pre-installed
FROM jekyll/jekyll:4.2.0

# Set the working directory to the root of your Jekyll project
WORKDIR /srv/jekyll

# Copy the Gemfile and Gemfile.lock to the container
#COPY Gemfile ./

# Install the project dependencies
#RUN bundle config --global jobs $(nproc) && bundle install

#RUN bundle install

# Copy the entire project directory to the container
COPY . .

# Build the Jekyll site
RUN jekyll build --trace

# Expose the default Jekyll port (4000)
EXPOSE 4000

# Set the command to run the Jekyll server
CMD ["jekyll", "serve", "--host", "0.0.0.0"]
# Use a base image with Ruby and other dependencies
FROM ruby:2.7.5

# Set the working directory in the container
WORKDIR /app

# Copy your Gemfile and Gemfile.lock into the container
COPY Gemfile Gemfile.lock ./

# Update Bundler to the latest version (Option 1)
RUN gem update --system

# Install the specific version of Bundler (Option 2)
# RUN gem install bundler:1.15.4

# Install Jekyll and other dependencies
RUN gem install bundler && bundle install

# Copy the rest of your website's source code into the container
COPY . .

# Expose the port your Jekyll server will run on
EXPOSE 4000

# Start the Jekyll server
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]

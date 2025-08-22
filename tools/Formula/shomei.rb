class Shomei < Formula
  desc "Show off your coding contributions without leaking corporate IP"
  homepage "https://github.com/petarran/shomei"
  url "https://github.com/petarran/shomei/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"  # This will be updated when we release
  license "MIT"
  head "https://github.com/petarran/shomei.git", branch: "main"

  depends_on "python@3.10"

  def install
    system "python3", "-m", "pip", "install", *std_pip_args, "."
  end

  test do
    system "#{bin}/shomei", "--help"
  end
end

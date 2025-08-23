class Shomei < Formula
  desc "Show off your coding contributions without leaking corporate IP"
  homepage "https://github.com/petarran/shomei"
  url "https://github.com/petarran/shomei/archive/refs/tags/v0.2.4.tar.gz"
  sha256 "4c74f3bdbf31640877ede87a808060fed8cbb349c266b4f1e9ac7bf26145db0f"
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

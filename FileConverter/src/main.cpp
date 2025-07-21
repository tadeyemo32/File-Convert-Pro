#include <iostream>
#include <string>
#include <filesystem>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <Magick++.h>
#include <stdexcept>
#include <cstdlib>

std::string toLower(const std::string &str)
{
  std::string lower = str;
  std::transform(lower.begin(), lower.end(), lower.begin(),
                 [](unsigned char c)
                 { return std::tolower(c); });
  return lower;
}

std::string getFileExtension(const std::string &filename)
{
  std::filesystem::path filePath(filename);
  return toLower(filePath.extension().string());
}

const std::unordered_map<std::string, std::vector<std::string>> conversionRules = {
    {".png", {"jpeg", "jpg", "webp", "bmp", "tiff"}},
    {".jpg", {"png", "jpeg", "webp", "bmp", "tiff"}},
    {".webp", {"jpeg", "png", "jpg", "bmp", "tiff"}},
    {".jpeg", {"jpg", "png", "webp", "bmp", "tiff"}},
    {".bmp", {"png", "jpg", "jpeg", "webp", "tiff"}},
    {".tiff", {"png", "jpg", "jpeg", "webp", "bmp"}},
    {".mp4", {"mp3", "gif"}},
    {".pdf", {"docx"}},
    {".docx", {"pdf"}}};

bool isImageConversion(const std::string &inputExt, const std::string &outputExt)
{
  const std::vector<std::string> imageExtensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"};
  return (std::find(imageExtensions.begin(), imageExtensions.end(), inputExt) != imageExtensions.end()) &&
         (std::find(imageExtensions.begin(), imageExtensions.end(), outputExt) != imageExtensions.end());
}

void convertMedia(const std::string &input, const std::string &output)
{
  std::string command;
  std::string outputExt = getFileExtension(output);

  if (outputExt == ".mp3")
  {
    command = "ffmpeg -i \"" + input + "\" -q:a 0 -map a \"" + output + "\"";
  }
  else if (outputExt == ".gif")
  {
    command = "ffmpeg -i \"" + input + "\" -vf \"fps=10,scale=640:-1:flags=lanczos\" \"" + output + "\"";
  }
  else
  {
    throw std::runtime_error("Unsupported media conversion");
  }

  int result = system(command.c_str());
  if (result != 0)
  {
    throw std::runtime_error("Media conversion failed with error code: " + std::to_string(result));
  }
  std::cout << "Successfully converted to: " << output << "\n";
}

void convertImage(const std::string &input, const std::string &output)
{
  try
  {
    Magick::InitializeMagick(nullptr);
    Magick::Image image;
    image.read(input);
    image.write(output);
    std::cout << "Successfully converted to: " << output << "\n";
  }
  catch (const std::exception &e)
  {
    throw std::runtime_error("Image conversion failed: " + std::string(e.what()));
  }
}

bool checkValidInput(const std::string &input, const std::string &outputType)
{
  if (!std::filesystem::exists(input))
  {
    std::cerr << "Error: Input file does not exist.\n";
    return false;
  }

  std::string inputExt = getFileExtension(input);
  std::string normalizedOutput = "." + toLower(outputType);

  if (inputExt.empty())
  {
    std::cerr << "Error: Input file has no extension.\n";
    return false;
  }

  auto it = conversionRules.find(inputExt);
  if (it == conversionRules.end())
  {
    std::cerr << "Error: Unsupported input file type.\n";
    return false;
  }

  const auto &validOutputs = it->second;
  if (std::find(validOutputs.begin(), validOutputs.end(), normalizedOutput.substr(1)) == validOutputs.end())
  {
    std::cerr << "Error: Unsupported conversion from " << inputExt << " to " << normalizedOutput << "\n";
    return false;
  }

  return true;
}

int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    std::cerr << "Usage: " << argv[0] << " <input-file> <output-type>\n";
    std::cerr << "Example: " << argv[0] << " input.jpg png\n";
    return 1;
  }

  std::string inputFile = argv[1];
  std::string outputType = toLower(argv[2]);

  try
  {
    if (!checkValidInput(inputFile, outputType))
    {
      return 1;
    }

    std::filesystem::path inputPath(inputFile);
    std::string outputFile = inputPath.stem().string() + "_converted." + outputType;
    std::string inputExt = getFileExtension(inputFile);
    std::string outputExt = "." + outputType;

    std::cout << "Converting " << inputFile << " to " << outputFile << "...\n";

    if (isImageConversion(inputExt, outputExt))
    {
      convertImage(inputFile, outputFile);
    }
    else
    {
      convertMedia(inputFile, outputFile);
    }

    return 0;
  }
  catch (const std::exception &e)
  {
    std::cerr << "Error: " << e.what() << "\n";
    return 1;
  }
}
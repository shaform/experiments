package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"github.com/schollz/progressbar"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
)

type Plurk struct {
	PlurkId       int
	Content       string
	Posted        string
	ResponseCount int
	Responses     []PlurkResponse
}

type PlurkResponse struct {
	Id      int
	Handle  string
	Content string
	Posted  string
}

// FetchResponses fetches responses of a given plurk
func FetchResponses(client *http.Client, plurkId int) ([]PlurkResponse, error) {
	const fetchUrl = "https://www.plurk.com/Responses/get2"

	data := url.Values{}
	data.Set("plurk_id", strconv.Itoa(plurkId))
	data.Set("from_response", "0")
	req, _ := http.NewRequest("POST", fetchUrl, strings.NewReader(data.Encode()))
	req.Header.Set("X-Requested-With", "XMLHttpRequest")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")

	// fetch responses
	resp, err := client.Do(req)
	if err != nil || resp.StatusCode != 200 {
		return []PlurkResponse{}, errors.New("connot load")
	}
	defer resp.Body.Close()

	content, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return []PlurkResponse{}, errors.New("connot load")
	}

	result := ParseJson(content)
	var responses []PlurkResponse
	for _, value := range result["responses"].([]interface{}) {
		switch obj := value.(type) {
		case map[string]interface{}:
			response := PlurkResponse{
				Id:      int(obj["id"].(float64)),
				Handle:  obj["handle"].(string),
				Content: obj["content"].(string),
				Posted:  obj["posted"].(string),
			}
			responses = append(responses, response)
		default:
		}
	}
	return responses, nil
}

// FetchAndSavePlurks queries plurk.com to
// obtain responsese from each plurk and
// save them to disk
func FetchAndSavePlurks(outputDir string, plurks []Plurk, delay int) {
	client := http.Client{Timeout: time.Second * 15}
	bar := progressbar.New(len(plurks))
	for _, plurk := range plurks {
		var responses []PlurkResponse
		var err error
		if plurk.ResponseCount > 0 {
			responses, err = FetchResponses(&client, plurk.PlurkId)
		}
		if err != nil {
			log.Printf("[WARN] Responses from %d cannot be fetched\n", plurk.PlurkId)
		} else {
			plurk.Responses = responses
			plurkJson, _ := json.Marshal(plurk)
			ioutil.WriteFile(fmt.Sprintf("%s/%d.json", outputDir, plurk.PlurkId), plurkJson, 0644)
		}
		bar.Add(1)
		if delay > 0 {
			time.Sleep(time.Millisecond * time.Duration(delay))
		}
	}
}

// ProcessPlurks parses the timeline,
// and produces a list of plurks.
func ProcessPlurks(result map[string]interface{}) []Plurk {
	var plurks []Plurk
	for _, value := range result {
		// Each value is an interface{} type, that is type asserted as a string
		switch obj := value.(type) {
		case map[string]interface{}:
			plurk := Plurk{
				PlurkId:       int(obj["plurk_id"].(float64)),
				Content:       obj["content"].(string),
				Posted:        obj["posted"].(string),
				ResponseCount: int(obj["response_count"].(float64))}
			plurks = append(plurks, plurk)
		default:
		}
	}

	return plurks
}

func ParseJson(inputs []byte) map[string]interface{} {
	var result map[string]interface{}
	json.Unmarshal(inputs, &result)

	return result
}

// GetPlurksFromFile loads json file
// to obtain plurk timeline.
func GetPlurksFromFile(path string) map[string]interface{} {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	content, err := ioutil.ReadAll(file)
	if err != nil {
		log.Fatal(err)
	}

	return ParseJson(content)
}

// GetPlurksFromFile queris uri
// to obtain plurk timeline.
func GetPlurks(uri string) map[string]interface{} {
	client := http.Client{Timeout: time.Second * 15}
	resp, err := client.Get(uri)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	content, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	return ParseJson(content)
}

func main() {
	const startUrl = "https://www.plurk.com/Stats/getAnonymousPlurks?lang=%s"

	// parse args
	var lang = flag.String("lang", "zh", "language of Plurks")
	var outputDir = flag.String("output-dir", "output", "directory for output")
	var file = flag.String("file", "", "read file instead of query URL")
	var delay = flag.Int("delay", 1000, "delay between each request in milliseconds")
	flag.Parse()

	// get plurks
	var result map[string]interface{}
	if *file != "" {
		result = GetPlurksFromFile(*file)
	} else {
		uri := fmt.Sprintf(startUrl, *lang)
		result = GetPlurks(uri)
	}

	plurks := ProcessPlurks(result)

	// start storing content...
	os.MkdirAll(*outputDir, 0700)
	FetchAndSavePlurks(*outputDir, plurks, *delay)
}

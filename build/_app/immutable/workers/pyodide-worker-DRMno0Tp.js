(function(){let e=`
import sys
import io
import json
import base64
import traceback
import numpy as np

class OutputCapture:
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self._old_stdout = None
        self._old_stderr = None

    def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def get_stdout(self):
        return self.stdout.getvalue()

    def get_stderr(self):
        return self.stderr.getvalue()
`,t=null,n=null;async function r(){return t||n||(n=(async()=>{self.postMessage({type:`status`,status:`loading_runtime`});let n=(await Function(`url`,`return import(url)`)(`https://cdn.jsdelivr.net/pyodide/v0.27.2/full/pyodide.mjs`)).loadPyodide;return t=await n({indexURL:`https://cdn.jsdelivr.net/pyodide/v0.27.2/full/`}),self.postMessage({type:`status`,status:`loading_packages`}),await t.loadPackage([`numpy`]),await t.runPythonAsync(e),self.postMessage({type:`status`,status:`ready`}),t})(),n)}function i(e){try{return btoa(unescape(encodeURIComponent(e)))}catch{return Buffer.from(e,`utf-8`).toString(`base64`)}}self.onmessage=async t=>{let n=new Set([self.location.origin,`null`]),a=typeof t.origin==`string`?t.origin:``;if(a&&!n.has(a)){self.postMessage({type:`error`,error:`Untrusted message origin: ${a}`});return}let{id:o,action:s,code:c,testHarnessCode:l,contentId:u,sampleLimit:d}=t.data;try{let t=await r();if(s===`init`){self.postMessage({id:o,type:`init_complete`,success:!0});return}if(s===`run`){self.postMessage({type:`status`,status:`running`});let n=performance.now(),r=i(c||``),a=`${e}

def __run_user_code():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        try:
            raw_code = base64.b64decode("${r}").decode("utf-8")
            exec(raw_code, exec_globals)
            err = None
        except Exception as e:
            err = traceback.format_exc()
        return {
            "stdout": cap.get_stdout(),
            "stderr": cap.get_stderr(),
            "error": err
        }

json.dumps(__run_user_code())
`,s=await t.runPythonAsync(a),l=JSON.parse(s),u=Math.round(performance.now()-n);self.postMessage({id:o,type:`run_result`,success:!l.error,output:l.stdout+(l.stderr?`
[STDERR]
`+l.stderr:``),error:l.error,durationMs:u}),self.postMessage({type:`status`,status:`ready`});return}if(s===`test`){self.postMessage({type:`status`,status:`testing`});let n=performance.now(),r=i(c||``),a=i(l||``),s=typeof d==`number`&&d>0,f=`${e}

def __run_module_tests():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        results = []
        raw_error = None
        try:
            # 1. Execute student code
            raw_code = base64.b64decode("${r}").decode("utf-8")
            exec(raw_code, exec_globals)

            # 2. Execute test harness
            raw_test = base64.b64decode("${a}").decode("utf-8")
            exec(raw_test, exec_globals)

            # 3. Call run_tests()
            if "run_tests" in exec_globals and callable(exec_globals["run_tests"]):
                results = exec_globals["run_tests"](${s?String(d):``})
            else:
                raw_error = "Test harness does not contain a run_tests() function."
        except Exception as e:
            raw_error = traceback.format_exc()

        return {
            "stdout": cap.get_stdout(),
            "stderr": cap.get_stderr(),
            "error": raw_error,
            "results": results
        }

json.dumps(__run_module_tests())
`,p=await t.runPythonAsync(f),m=JSON.parse(p),h=Math.round(performance.now()-n),g=(m.results||[]).map(e=>({name:e.name,passed:!!e.passed,durationMs:e.durationMs||1,error:e.error||void 0})),_=g.filter(e=>e.passed).length,v=g.length,y=!m.error&&v>0&&_===v;self.postMessage({id:o,type:`test_result`,contentId:u,isSample:s,allPassed:y,totalTests:v,passedTests:_,failedTests:v-_,totalDurationMs:h,results:g,rawOutput:m.stdout+(m.stderr?`
`+m.stderr:``),error:m.error}),self.postMessage({type:`status`,status:`ready`});return}}catch(e){self.postMessage({id:o,type:`error`,error:e?.message||String(e)}),self.postMessage({type:`status`,status:`ready`})}}})();
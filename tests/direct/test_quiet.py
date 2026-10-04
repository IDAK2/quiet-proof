from conftest import CONTRACT
URLS=['https://status-one.example/archive','https://status-two.example/log']
def setup(vm,deploy,a):
 vm.warp('2035-01-01T00:00:00+00:00');vm.sender=a;c=deploy(CONTRACT);c.open_probe('quiet-7','Public maintenance notices for the north bridge','A notice explicitly announcing a closure of the north bridge',URLS,2051222460);return c
def mocks(vm,labels='["ABSENT","ABSENT"]',valid=True):
 vm.mock_web(r'status-one\.example',{'status':200,'body':'North bridge maintenance archive: inspections continue; no closure announced.'});vm.mock_web(r'status-two\.example',{'status':200,'body':'Transport log covers north bridge and lists normal access.'});vm.mock_llm(r'.*QuietProof observer.*','{"labels":'+labels+'}');vm.mock_llm(r'.*QuietProof verifier.*','{"valid":'+str(valid).lower()+'}')
def test_all_sources_required_for_absence(direct_vm,direct_deploy,direct_alice):
 c=setup(direct_vm,direct_deploy,direct_alice);direct_vm.warp('2035-01-01T00:01:01+00:00');mocks(direct_vm);c.observe('quiet-7');r=c.get_probe('quiet-7');assert r['state']=='ABSENT' and r['labels']==['ABSENT','ABSENT'] and len(r['digests'])==2
def test_present_source_overrides_absence(direct_vm,direct_deploy,direct_alice):
 c=setup(direct_vm,direct_deploy,direct_alice);direct_vm.warp('2035-01-01T00:01:01+00:00');mocks(direct_vm,'["ABSENT","PRESENT"]');c.observe('quiet-7');assert c.get_probe('quiet-7')['state']=='PRESENT'
def test_mixed_ambiguous_is_inconclusive(direct_vm,direct_deploy,direct_alice):
 c=setup(direct_vm,direct_deploy,direct_alice);direct_vm.warp('2035-01-01T00:01:01+00:00');mocks(direct_vm,'["ABSENT","AMBIGUOUS"]');c.observe('quiet-7');assert c.get_probe('quiet-7')['state']=='INCONCLUSIVE'
def test_distinct_origins_and_due_time_enforced(direct_vm,direct_deploy,direct_alice):
 direct_vm.warp('2035-01-01T00:00:00+00:00');direct_vm.sender=direct_alice;c=direct_deploy(CONTRACT)
 with direct_vm.expect_revert('independent sources'):c.open_probe('bad','A sufficiently detailed public subject','A sufficiently detailed signal',['https://same.example/a','https://same.example/b'],2051222460)
 c.open_probe('ok','A sufficiently detailed public subject','A sufficiently detailed signal',URLS,2051222460)
 with direct_vm.expect_revert('due unobserved'):c.observe('ok')
def test_validator_rejects_forged_labels_and_digests(direct_vm,direct_deploy,direct_alice):
 c=setup(direct_vm,direct_deploy,direct_alice);mocks(direct_vm);r=c._observe(c.probes['QUIET-7']);assert direct_vm.run_validator(leader_result=r) is True
 forged=dict(r);forged['labels']=['PRESENT','PRESENT'];direct_vm.clear_mocks();mocks(direct_vm,valid=False);assert direct_vm.run_validator(leader_result=forged) is False
 forged2=dict(r);forged2['digests']=['0'*64,'1'*64];assert direct_vm.run_validator(leader_result=forged2) is False
def test_owner_cancel_and_duplicate_id(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice);direct_vm.sender=direct_bob
 with direct_vm.expect_revert('owner may cancel'):c.cancel('quiet-7')
 direct_vm.sender=direct_alice;c.cancel('quiet-7');assert c.get_probe('quiet-7')['state']=='CANCELLED'
 with direct_vm.expect_revert('unique probe'):c.open_probe('quiet-7','Another sufficiently detailed subject','Another sufficiently detailed signal',URLS,2051222500)

